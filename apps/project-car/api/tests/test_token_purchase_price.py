"""AUD-001: the server prices a token purchase. A client amount is not the price."""

from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy import func, select

from app.config import get_settings
from app.models import BillingTransaction, TokenTransaction, TokenTransactionKind
from app.services.payments import STAND_IN_PACKS
from tests.conftest import create_member, login_member

REPRO = {"tokens": "999999", "amount_cad": "0.01", "payment_id": "STANDIN-REPRO"}


def _buyer(client: TestClient, email: str) -> str:
    member = create_member(client, email=email, tier_name="basic")
    login_member(client, member["email"])
    return member["id"]


def _counts(client: TestClient, member_id: str) -> tuple[int, int]:
    session = client.session_factory()  # type: ignore[attr-defined]
    mid = UUID(member_id)
    try:
        billing = session.scalar(
            select(func.count()).select_from(BillingTransaction).where(BillingTransaction.member_id == mid)
        )
        ledger = session.scalar(
            select(func.count()).select_from(TokenTransaction).where(
                TokenTransaction.member_id == mid,
                TokenTransaction.kind == TokenTransactionKind.TOKEN_PURCHASE,
            )
        )
    finally:
        session.close()
    return int(billing or 0), int(ledger or 0)


def test_client_chosen_amount_is_rejected(client: TestClient) -> None:
    """999,999 tokens for 0.01 CAD is the audit repro. A different token count is too."""
    member_id = _buyer(client, "price-client@example.com")
    bought = client.post("/member/token-purchases", json=REPRO)
    assert bought.status_code == 422, bought.text
    assert bought.json()["error"]["code"] == "amount_mismatch"
    pack = STAND_IN_PACKS[0]
    other = client.post(
        "/member/token-purchases",
        json={
            "payment_id": "STANDIN-TOKENS",
            "tokens": format(pack.tokens + 1, "f"),
            "amount_cad": format(pack.amount_cad, "f"),
        },
    )
    assert other.status_code == 422 and other.json()["error"]["code"] == "amount_mismatch", other.text
    assert _counts(client, member_id) == (0, 0)


def test_purchase_not_configured_outside_dev_mode(client: TestClient, monkeypatch) -> None:
    member_id = _buyer(client, "price-prod@example.com")
    monkeypatch.delenv("SHOP_DEV_MODE", raising=False)
    get_settings.cache_clear()
    try:
        bought = client.post("/member/token-purchases", json=REPRO)
        assert bought.status_code == 503, bought.text
        assert bought.json()["error"]["code"] == "purchase_not_configured"
        assert _counts(client, member_id) == (0, 0)
    finally:
        get_settings.cache_clear()


def test_dev_mode_records_the_stand_in_pack(client: TestClient) -> None:
    pack = STAND_IN_PACKS[0]
    assert (pack.id, pack.tokens, pack.amount_cad, pack.label) == (
        "stand-in", Decimal("10"), Decimal("1.00"), "not a real price",
    )
    member_id = _buyer(client, "price-pack@example.com")
    bought = client.post(
        "/member/token-purchases",
        json={
            "payment_id": "STANDIN-PACK",
            "tokens": format(pack.tokens, "f"),
            "amount_cad": format(pack.amount_cad, "f"),
        },
    )
    assert bought.status_code == 201, bought.text
    body = bought.json()
    assert Decimal(str(body["amount"])) == pack.tokens
    assert body["note"] == pack.label
    assert Decimal(body["meta"]["purchase"]["amount_cad"]) == pack.amount_cad
    me = client.get("/member/me")
    assert Decimal(str(me.json()["purchased_balance"])) == pack.tokens
    assert _counts(client, member_id) == (1, 1)
