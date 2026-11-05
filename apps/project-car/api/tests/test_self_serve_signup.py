"""Self-serve signup and a stand-in token purchase.

Red on main: POST /signup is not a route, and Settings has no payment
processor field and no registry, so an unknown name is not 422.
"""

from __future__ import annotations

import importlib.util
from decimal import Decimal
from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, func, select, text
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import BillingTransaction, TokenTransaction, TokenTransactionKind
from tests.conftest import AUTH, create_member, login_member

API_ROOT = Path(__file__).resolve().parents[1]
VERSIONS = API_ROOT / "alembic" / "versions"
ALEMBIC_INI = API_ROOT / "alembic.ini"

EMAIL = "self.serve@example.com"
PASSWORD = "walkthrough-pass"


def _session(client: TestClient) -> Session:
    return client.session_factory()  # type: ignore[attr-defined]


def _signup(client: TestClient, **overrides: object):
    body = {
        "name": "Self Serve",
        "email": EMAIL,
        "phone": "403-555-0199",
        "password": PASSWORD,
        "tier_name": "basic",
    }
    body.update(overrides)
    return client.post("/signup", json=body)


def test_self_serve_signup_creates_a_basic_member(client: TestClient) -> None:
    mode = client.get("/signup-mode")
    assert mode.status_code == 200, mode.text
    assert mode.json()["mode"] == "self_serve"

    signed = _signup(client)
    assert signed.status_code == 201, signed.text
    body = signed.json()
    assert body["mode"] == "self_serve"
    assert body["tier_name"] == "basic"
    assert body["email"] == EMAIL
    member_id = body["member_id"]
    assert member_id

    me = client.get("/member/me")
    assert me.status_code == 200, me.text
    profile = me.json()
    assert profile["id"] == member_id
    assert profile["tier_name"] == "basic"
    assert profile["status"] == "active"
    assert Decimal(str(profile["allowance_balance"])) == Decimal("1000")
    assert Decimal(str(profile["purchased_balance"])) == Decimal("0")
    assert Decimal(str(profile["token_balance"])) == Decimal("1000")
    assert [row["kind"] for row in profile["tokens"]] == ["monthly_allocation"]

    logged = client.post("/auth/member/login", json={"email": EMAIL, "password": PASSWORD})
    assert logged.status_code == 200, logged.text

    waitlist = client.get("/waitlist", headers=AUTH)
    assert waitlist.status_code == 200, waitlist.text
    assert all(row["email"] != EMAIL for row in waitlist.json())


def test_waitlist_mode_creates_a_waitlist_row(client: TestClient) -> None:
    switched = client.patch("/signup-mode", headers=AUTH, json={"mode": "waitlist"})
    assert switched.status_code == 200, switched.text
    assert switched.json()["mode"] == "waitlist"

    signed = _signup(client, email="fallback@example.com", password=None)
    assert signed.status_code == 201, signed.text
    body = signed.json()
    assert body["mode"] == "waitlist"
    assert body["member_id"] is None
    assert body["waitlist_id"]

    members = client.get("/members", headers=AUTH)
    assert members.status_code == 200, members.text
    assert all(row["email"] != "fallback@example.com" for row in members.json())
    waitlist = client.get("/waitlist", headers=AUTH)
    assert any(row["email"] == "fallback@example.com" for row in waitlist.json())

    restored = client.patch("/signup-mode", headers=AUTH, json={"mode": "self_serve"})
    assert restored.status_code == 200, restored.text
    assert restored.json()["mode"] == "self_serve"


def test_unknown_signup_mode_reads_as_self_serve(client: TestClient) -> None:
    from app.models import ShopSetting

    session = _session(client)
    session.add(ShopSetting(key="signup_mode", value="banana"))
    session.commit()
    session.close()

    mode = client.get("/signup-mode")
    assert mode.status_code == 200, mode.text
    assert mode.json()["mode"] == "self_serve"


def test_unknown_processor_is_422(client: TestClient, monkeypatch) -> None:
    monkeypatch.setenv("PAYMENT_PROCESSOR", "not-a-processor")
    get_settings.cache_clear()
    try:
        member = create_member(client, email="buyer-unknown@example.com", tier_name="basic")
        login_member(client, member["email"])
        bought = client.post(
            "/member/token-purchases",
            json={
                "payment_id": "STANDIN-SHOULD-NOT-RUN",
                "tokens": "10.00",
                "amount_cad": "5.00",
            },
        )
        assert bought.status_code == 422, bought.text
        error = bought.json()["error"]
        assert error["code"] == "unknown_processor"
        assert "not-a-processor" in error["message"]
    finally:
        get_settings.cache_clear()


def test_stand_in_purchase_writes_one_billing_row_and_one_ledger_row(
    client: TestClient, monkeypatch
) -> None:
    monkeypatch.setenv("PAYMENT_PROCESSOR", "stand-in")
    get_settings.cache_clear()
    try:
        member = create_member(client, email="buyer@example.com", tier_name="basic")
        login_member(client, member["email"])
        bought = client.post(
            "/member/token-purchases",
            json={
                "payment_id": "STANDIN-PACK-1",
                "tokens": "200.00",
                "amount_cad": "40.00",
            },
        )
        assert bought.status_code == 201, bought.text
        purchase = bought.json()
        assert purchase["kind"] == "token_purchase"
        assert Decimal(str(purchase["amount"])) == Decimal("200.00")
        meta = purchase["meta"]["purchase"]
        assert meta["processor"] == "stand-in"
        assert meta["payment_id"] == "STANDIN-PACK-1"
        assert Decimal(meta["amount_cad"]) == Decimal("40.00")
        assert meta["fee_rate"] == "stand-in-none"
        assert "gst" not in meta

        me = client.get("/member/me")
        assert me.status_code == 200, me.text
        profile = me.json()
        assert Decimal(str(profile["allowance_balance"])) == Decimal("1000")
        assert Decimal(str(profile["purchased_balance"])) == Decimal("200.00")
        assert Decimal(str(profile["token_balance"])) == (
            Decimal(str(profile["allowance_balance"])) + Decimal(str(profile["purchased_balance"]))
        )

        session = _session(client)
        member_id = member["id"]
        billing = session.scalars(
            select(BillingTransaction).where(BillingTransaction.member_id == member_id)
        ).all()
        assert len(billing) == 1
        assert billing[0].kind.value == "pack"
        assert Decimal(str(billing[0].amount)) == Decimal("40.00")
        assert billing[0].note
        ledger = session.scalars(
            select(TokenTransaction).where(
                TokenTransaction.member_id == member_id,
                TokenTransaction.kind == TokenTransactionKind.TOKEN_PURCHASE,
            )
        ).all()
        assert len(ledger) == 1
        assert ledger[0].payment_ref == "STANDIN-PACK-1"
        assert Decimal(str(ledger[0].purchased_amount)) == Decimal("200.00")
        assert Decimal(str(ledger[0].allowance_amount)) == Decimal("0")
        session.close()

        refused = client.post(
            "/member/token-purchases",
            json={"payment_id": "PAYPAL-LIVE-1", "tokens": "10.00", "amount_cad": "5.00"},
        )
        assert refused.status_code == 422, refused.text
        assert refused.json()["error"]["code"] == "standin_only"

        again = client.post(
            "/member/token-purchases",
            json={
                "payment_id": "STANDIN-PACK-1",
                "tokens": "200.00",
                "amount_cad": "40.00",
            },
        )
        assert again.status_code == 409, again.text
        assert again.json()["error"]["code"] == "already_credited"

        session = _session(client)
        billing_count = session.scalar(
            select(func.count())
            .select_from(BillingTransaction)
            .where(BillingTransaction.member_id == member_id)
        )
        ledger_count = session.scalar(
            select(func.count())
            .select_from(TokenTransaction)
            .where(
                TokenTransaction.member_id == member_id,
                TokenTransaction.kind == TokenTransactionKind.TOKEN_PURCHASE,
            )
        )
        session.close()
        assert billing_count == 1
        assert ledger_count == 1
    finally:
        get_settings.cache_clear()


def test_signup_mode_migration_inserts_self_serve() -> None:
    path = VERSIONS / "20261105_0019_signup_mode.py"
    assert path.is_file(), path

    spec = importlib.util.spec_from_file_location("signup_mode_revision", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.revision == "20261105_0019"
    assert module.down_revision == "20261105_0018"

    from alembic.config import Config
    from alembic.operations import Operations
    from alembic.runtime.migration import MigrationContext
    from alembic.script import ScriptDirectory

    script = ScriptDirectory.from_config(Config(str(ALEMBIC_INI)))
    assert script.get_heads() == ["20261105_0019"]

    engine = create_engine("sqlite://")
    with engine.begin() as connection:

        def _apply(fn) -> None:
            ctx = MigrationContext.configure(connection)
            with Operations.context(ctx):
                fn()

        def _mode() -> str | None:
            return connection.execute(
                text("SELECT value FROM shop_settings WHERE key = 'signup_mode'")
            ).scalar()

        _apply(module.upgrade)
        assert _mode() == "self_serve"
        _apply(module.downgrade)
        table = connection.execute(
            text("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'shop_settings'")
        ).scalar()
        assert table is None
        _apply(module.upgrade)
        assert _mode() == "self_serve"
