"""Paid tokens land as one ``token_purchase`` row tied to the PayPal payment id.

``POST /members/{id}/token-purchases`` (human Owner only) credits the tokens,
stores the payment id on the row, and records subtotal, GST at
``GST_RATE`` and total in ``meta``. The same payment id twice is 409
``already_credited`` and writes nothing.

The ledger also refuses a second reserve, refund or debit for one booking at
the database: a unique index on (booking_id, kind) for those kinds.

Payment ids and CAD amounts here are stand-ins, not real PayPal values.
"""

from __future__ import annotations

import importlib.util
from decimal import Decimal
from pathlib import Path
from uuid import UUID

import pytest
from alembic.operations import Operations
from alembic.runtime.migration import MigrationContext
from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect, text

from app.models import Member, TokenTransactionKind
from app.services import tokens as token_service
from tests.conftest import AUTH, create_hoist, create_member, next_hour

AI = {"Authorization": "Bearer dev-ai-secret"}
STAND_IN_PAYMENT = "STANDIN-PAYPAL-0001"


def _ledger(client: TestClient, member_id: str) -> list[dict]:
    response = client.get(f"/members/{member_id}/tokens", headers=AUTH)
    assert response.status_code == 200, response.text
    return response.json()


def _balance(client: TestClient, member_id: str) -> Decimal:
    return Decimal(str(client.get(f"/members/{member_id}", headers=AUTH).json()["token_balance"]))


def _purchase(client: TestClient, member_id: str, **overrides):
    body = {
        "payment_id": STAND_IN_PAYMENT,
        "tokens": "500",
        "subtotal_cad": "40.00",
        **overrides,
    }
    return client.post(f"/members/{member_id}/token-purchases", headers=AUTH, json=body)


def test_purchase_credits_once_per_payment_id(client: TestClient) -> None:
    member = create_member(client, email="buyer@example.com")
    before = _balance(client, member["id"])

    first = _purchase(client, member["id"])
    assert first.status_code == 201, first.text
    row = first.json()
    assert row["kind"] == "token_purchase"
    assert Decimal(str(row["amount"])) == Decimal("500")
    assert row["payment_ref"] == STAND_IN_PAYMENT
    assert row["meta"]["purchase"] == {
        "payment_id": STAND_IN_PAYMENT,
        "subtotal_cad": "40.00",
        "gst_rate": "0.05",
        "gst_cad": "2.00",
        "total_cad": "42.00",
        "by": "owner@projectcar.ca",
    }
    assert _balance(client, member["id"]) == before + Decimal("500")
    rows_after_first = _ledger(client, member["id"])

    for payment_id in (STAND_IN_PAYMENT, f"  {STAND_IN_PAYMENT} "):
        again = _purchase(client, member["id"], payment_id=payment_id)
        assert again.status_code == 409, again.text
        assert again.json()["error"]["code"] == "already_credited"
    assert _ledger(client, member["id"]) == rows_after_first
    assert _balance(client, member["id"]) == before + Decimal("500")


def test_same_payment_id_cannot_credit_a_second_member(client: TestClient) -> None:
    ada = create_member(client, email="ada-buy@example.com")
    sam = create_member(client, email="sam-buy@example.com")
    assert _purchase(client, ada["id"]).status_code == 201
    other = _purchase(client, sam["id"])
    assert other.status_code == 409, other.text
    assert other.json()["error"]["code"] == "already_credited"


def test_gst_rounds_half_up_to_the_cent(client: TestClient) -> None:
    member = create_member(client, email="gst@example.com")
    response = _purchase(client, member["id"], payment_id="STANDIN-PAYPAL-0002", subtotal_cad="12.30")
    assert response.status_code == 201, response.text
    purchase = response.json()["meta"]["purchase"]
    # 12.30 x 0.05 = 0.615 -> 0.62
    assert purchase["gst_cad"] == "0.62"
    assert purchase["total_cad"] == "12.92"


def test_gst_rate_stand_in_is_five_percent() -> None:
    assert token_service.GST_RATE == Decimal("0.05")


@pytest.mark.parametrize(
    "overrides",
    [
        {"payment_id": "  "},
        {"tokens": "0"},
        {"tokens": "-5"},
        {"tokens": "1.005"},
        {"subtotal_cad": "-1.00"},
        {"subtotal_cad": "1.001"},
    ],
)
def test_bad_purchase_is_refused_and_writes_nothing(client: TestClient, overrides: dict) -> None:
    member = create_member(client, email="bad-buy@example.com")
    before = _ledger(client, member["id"])
    response = _purchase(client, member["id"], **overrides)
    assert response.status_code in (400, 422), response.text
    assert _ledger(client, member["id"]) == before


def test_ai_cannot_record_a_purchase(client: TestClient) -> None:
    member = create_member(client, email="ai-buy@example.com")
    before = _ledger(client, member["id"])
    response = client.post(
        f"/members/{member['id']}/token-purchases",
        headers=AI,
        json={"payment_id": STAND_IN_PAYMENT, "tokens": "500", "subtotal_cad": "40.00"},
    )
    assert response.status_code == 403, response.text
    assert response.json()["error"]["code"] == "token_change_requires_human"
    assert _ledger(client, member["id"]) == before


def _cancelled_booking(client: TestClient) -> tuple[dict, dict]:
    member = create_member(client, email="refund-once@example.com")
    bay = create_hoist(client, name="Bay 1")
    start = next_hour(4)
    created = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": bay["id"],
            "start_at": start.isoformat(),
            "end_at": next_hour(5).isoformat(),
        },
    )
    assert created.status_code == 201, created.text
    cancelled = client.post(f"/bookings/{created.json()['id']}/cancel", headers=AUTH, json={"reason": "Owner cancelled this visit"})
    assert cancelled.status_code == 200, cancelled.text
    return member, created.json()


@pytest.mark.parametrize(
    ("kind", "amount"),
    [
        (TokenTransactionKind.BOOKING_REFUND, Decimal("100")),
        (TokenTransactionKind.BOOKING_RESERVE, Decimal("-100")),
    ],
)
def test_second_booking_row_of_a_kind_is_rejected_by_the_ledger(
    client: TestClient, kind: TokenTransactionKind, amount: Decimal
) -> None:
    member, booking = _cancelled_booking(client)
    rows_before = _ledger(client, member["id"])
    balance_before = _balance(client, member["id"])

    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        row = session.get(Member, UUID(member["id"]))
        with pytest.raises(HTTPException) as caught:
            token_service.apply_ledger(
                session,
                row,
                kind=kind,
                amount=amount,
                booking_id=UUID(booking["id"]),
                note="Second row for the same booking",
            )
        assert caught.value.status_code == 409
        assert caught.value.detail["code"] == "duplicate_ledger_entry"
    finally:
        session.close()

    assert _ledger(client, member["id"]) == rows_before
    assert _balance(client, member["id"]) == balance_before


def _migration():
    path = (
        Path(__file__).resolve().parents[1]
        / "alembic"
        / "versions"
        / "20261031_0017_token_purchase_and_ledger_guards.py"
    )
    spec = importlib.util.spec_from_file_location("token_purchase_20261031_0017", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_migration_adds_payment_ref_and_ledger_guards() -> None:
    module = _migration()
    assert module.revision == "20261031_0017"
    assert module.down_revision == "20261023_0016"

    engine = create_engine("sqlite://")
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                CREATE TABLE token_transactions (
                    id TEXT PRIMARY KEY,
                    member_id TEXT NOT NULL,
                    booking_id TEXT,
                    kind VARCHAR(40) NOT NULL,
                    amount NUMERIC(12, 2) NOT NULL,
                    note TEXT,
                    meta JSON,
                    created_at DATETIME NOT NULL
                )
                """
            )
        )
        context = MigrationContext.configure(connection)
        with Operations.context(context):
            module.upgrade()
        columns = {column["name"] for column in inspect(connection).get_columns("token_transactions")}
        indexes = {index["name"] for index in inspect(connection).get_indexes("token_transactions")}
        assert "payment_ref" in columns
        assert {"uq_token_transactions_payment_ref", "uq_token_transactions_booking_kind"} <= indexes

        with Operations.context(context):
            module.downgrade()
        columns = {column["name"] for column in inspect(connection).get_columns("token_transactions")}
        assert "payment_ref" not in columns
