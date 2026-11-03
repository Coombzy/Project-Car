"""Owner balance overrides carry a reason and an actor; balances never go below zero.

- An Owner token adjustment needs ``reason`` (3-500 characters after strip),
  else 422 ``reason_required``. The row stores ``meta.override = {reason, by}``.
- No ledger write may leave a balance under ``TOKEN_BALANCE_FLOOR`` (0). An
  adjustment that would is 409 ``would_go_negative``; there is no allow flag
  (Ben, D10).
- Completing a visit charges the full reserve. Unused time is never refunded
  once a booking has started (Ben, D16): a positive ``unused_tokens`` is 400
  ``unused_refund_not_allowed`` and completion writes no refund row.
"""

from __future__ import annotations

from datetime import timedelta
from decimal import Decimal
from uuid import UUID

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.models import Member, TokenTransactionKind
from app.services import tokens as token_service
from tests.conftest import AUTH, check_in_open_start, create_hoist, create_member

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


def _active_booking(client: TestClient) -> tuple[dict, dict]:
    member = create_member(client, email="complete@example.com")
    bay = create_hoist(client, name="Bay 1")
    start = check_in_open_start()
    created = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": bay["id"],
            "start_at": start.isoformat(),
            "end_at": (start + timedelta(hours=2)).isoformat(),
        },
    )
    assert created.status_code == 201, created.text
    booking = created.json()
    assert client.post(f"/bookings/{booking['id']}/confirm", headers=AUTH).status_code == 200
    checked = client.post(f"/bookings/{booking['id']}/check-in", headers=AUTH)
    assert checked.status_code == 200, checked.text
    return member, booking


def _booking_rows(client: TestClient, member_id: str, booking_id: str) -> list[str]:
    return sorted(row["kind"] for row in _ledger(client, member_id) if row["booking_id"] == booking_id)


@pytest.mark.parametrize("body", [None, {"unused_tokens": "0"}])
def test_complete_charges_the_full_reserve_and_writes_no_refund(
    client: TestClient, body: dict | None
) -> None:
    member, booking = _active_booking(client)
    balance = _balance(client, member["id"])

    completed = client.post(f"/bookings/{booking['id']}/complete", headers=AUTH, json=body)
    assert completed.status_code == 200, completed.text
    assert completed.json()["status"] == "completed"
    assert _booking_rows(client, member["id"], booking["id"]) == ["booking_reserve"]
    assert _balance(client, member["id"]) == balance


@pytest.mark.parametrize("unused", ["0.01", "50", "full"])
def test_complete_rejects_any_unused_refund(client: TestClient, unused: str) -> None:
    member, booking = _active_booking(client)
    if unused == "full":
        unused = str(booking["reserved_tokens"])
    balance = _balance(client, member["id"])

    response = client.post(
        f"/bookings/{booking['id']}/complete",
        headers=AUTH,
        json={"unused_tokens": unused, "reason": REASON},
    )
    assert response.status_code == 400, response.text
    assert response.json()["error"]["code"] == "unused_refund_not_allowed"
    stored = next(row for row in client.get("/bookings", headers=AUTH).json() if row["id"] == booking["id"])
    assert stored["status"] == "active"
    assert _booking_rows(client, member["id"], booking["id"]) == ["booking_reserve"]
    assert _balance(client, member["id"]) == balance
