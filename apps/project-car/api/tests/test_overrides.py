"""Owner balance overrides carry a reason and an actor; balances never go below zero.

- An Owner token adjustment needs ``reason`` (3-500 characters after strip),
  else 422 ``reason_required``. The row stores ``meta.override = {reason, by}``.
- No ledger write may leave a balance under ``TOKEN_BALANCE_FLOOR`` (0). An
  adjustment that would is 409 ``would_go_negative``; there is no allow flag
  (Ben, D10).
"""

from __future__ import annotations

from decimal import Decimal
from uuid import UUID

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.models import Member, TokenTransactionKind
from app.services import tokens as token_service
from tests.conftest import AUTH, create_member

REASON = "Goodwill credit for the bay 2 outage"


def _ledger(client: TestClient, member_id: str) -> list[dict]:
    response = client.get(f"/members/{member_id}/tokens", headers=AUTH)
    assert response.status_code == 200, response.text
    return response.json()


def _balance(client: TestClient, member_id: str) -> Decimal:
    return Decimal(str(client.get(f"/members/{member_id}", headers=AUTH).json()["token_balance"]))


def _adjust(client: TestClient, member_id: str, body: dict):
    return client.post(f"/members/{member_id}/tokens", headers=AUTH, json=body)


@pytest.mark.parametrize("reason", [None, "", "   ", "ab", "x" * 501])
def test_adjust_requires_reason(client: TestClient, reason: str | None) -> None:
    member = create_member(client, email="reason@example.com")
    before = _ledger(client, member["id"])
    body: dict = {"amount": "25"}
    if reason is not None:
        body["reason"] = reason
    response = _adjust(client, member["id"], body)
    assert response.status_code == 422, response.text
    assert response.json()["error"]["code"] == "reason_required"
    assert _ledger(client, member["id"]) == before


def test_adjust_records_reason_and_actor(client: TestClient) -> None:
    member = create_member(client, email="audit@example.com")
    response = _adjust(client, member["id"], {"amount": "25", "reason": f"  {REASON}  "})
    assert response.status_code == 201, response.text
    row = response.json()
    assert row["kind"] == "admin_adjustment"
    assert row["meta"]["override"] == {"reason": REASON, "by": "owner@projectcar.ca"}
    assert row["note"] == REASON


def test_adjust_below_zero_is_refused(client: TestClient) -> None:
    member = create_member(client, email="floor@example.com")
    balance = _balance(client, member["id"])
    before = _ledger(client, member["id"])

    for body in (
        {"amount": str(-(balance + Decimal("0.01"))), "reason": REASON},
        {"amount": "-5000", "reason": REASON, "allow_negative": True},
    ):
        response = _adjust(client, member["id"], body)
        assert response.status_code == 409, response.text
        error = response.json()["error"]
        assert error["code"] == "would_go_negative"
        assert Decimal(str(error["balance"])) == balance
    assert _ledger(client, member["id"]) == before
    assert _balance(client, member["id"]) == balance

    to_zero = _adjust(client, member["id"], {"amount": str(-balance), "reason": REASON})
    assert to_zero.status_code == 201, to_zero.text
    assert _balance(client, member["id"]) == Decimal("0")


def test_floor_guards_every_ledger_writer(client: TestClient) -> None:
    member = create_member(client, email="floor-writer@example.com")
    balance = _balance(client, member["id"])
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        row = session.get(Member, UUID(member["id"]))
        with pytest.raises(HTTPException) as caught:
            token_service.apply_ledger(
                session,
                row,
                kind=TokenTransactionKind.BOOKING_DEBIT,
                amount=-(balance + 1),
            )
        assert caught.value.status_code == 409
        assert caught.value.detail["code"] == "would_go_negative"
    finally:
        session.close()
    assert _balance(client, member["id"]) == balance
    assert token_service.TOKEN_BALANCE_FLOOR == Decimal("0")
