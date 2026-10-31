"""A visit that has started is not a refund. A missed visit is a no-show."""

from __future__ import annotations

from datetime import timedelta
from decimal import Decimal
from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy import select

from app.models import BookingHour
from tests.conftest import AUTH, create_hoist, create_member, freeze_shop_clock, login_member, next_hour

REASON = {"reason": "Owner cancelled this visit"}


def _confirmed(client: TestClient, *, hours_ahead: int = 30, length: int = 1) -> tuple[dict, dict, object]:
    member = create_member(client)
    hoist = create_hoist(client)
    start = next_hour(hours_ahead)
    login_member(client, member["email"])
    created = client.post(
        "/member/bookings",
        json={
            "hoist_id": hoist["id"],
            "start_at": start.isoformat(),
            "end_at": (start + timedelta(hours=length)).isoformat(),
        },
    )
    assert created.status_code == 201, created.text
    assert created.json()["status"] == "confirmed"
    return member, created.json(), start


def _balance(client: TestClient, member_id: str) -> Decimal:
    return Decimal(str(client.get(f"/members/{member_id}", headers=AUTH).json()["token_balance"]))


def _held(client: TestClient, booking_id: str) -> int:
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        return len(session.scalars(select(BookingHour).where(BookingHour.booking_id == UUID(booking_id))).all())
    finally:
        session.close()


def test_check_in_ten_minutes_early_then_cancel_keeps_the_balance(client: TestClient) -> None:
    member, booking, start = _confirmed(client)
    freeze_shop_clock(start - timedelta(minutes=10))
    checked = client.post(f"/bookings/{booking['id']}/check-in", headers=AUTH)
    assert checked.status_code == 200, checked.text
    before = _balance(client, member["id"])

    refused = client.post(f"/member/bookings/{booking['id']}/cancel")

    assert refused.status_code == 400, refused.text
    assert _balance(client, member["id"]) == before
    assert client.get("/bookings", headers=AUTH).json()[0]["status"] == "active"


def test_one_minute_past_the_end_frees_the_hour_and_keeps_the_tokens(client: TestClient) -> None:
    member, booking, start = _confirmed(client, length=1)
    freeze_shop_clock(start + timedelta(hours=1, minutes=1))
    before = _balance(client, member["id"])

    listed = client.get("/bookings", headers=AUTH)

    assert listed.status_code == 200, listed.text
    stored = next(row for row in listed.json() if row["id"] == booking["id"])
    assert stored["status"] == "no_show"
    assert _held(client, booking["id"]) == 0
    assert _balance(client, member["id"]) == before
    again = client.post("/bookings/sweep-no-shows", headers=AUTH)
    assert again.status_code == 200, again.text
    assert again.json() == []


def test_owner_cancel_after_the_start_is_not_a_refund(client: TestClient) -> None:
    member, booking, start = _confirmed(client, length=2)
    freeze_shop_clock(start + timedelta(minutes=1))
    before = _balance(client, member["id"])

    refused = client.post(f"/bookings/{booking['id']}/cancel", headers=AUTH, json=REASON)

    assert refused.status_code == 400, refused.text
    assert _balance(client, member["id"]) == before
    stored = next(row for row in client.get("/bookings", headers=AUTH).json() if row["id"] == booking["id"])
    assert stored["status"] == "confirmed"


def test_owner_cancel_requires_a_written_reason(client: TestClient) -> None:
    member, booking, _start = _confirmed(client, hours_ahead=30)
    before = _balance(client, member["id"])

    missing = client.post(f"/bookings/{booking['id']}/cancel", headers=AUTH)
    assert missing.status_code == 422, missing.text
    assert missing.json()["error"]["code"] == "reason_required"
    assert _balance(client, member["id"]) == before

    cancelled = client.post(f"/bookings/{booking['id']}/cancel", headers=AUTH, json=REASON)
    assert cancelled.status_code == 200, cancelled.text
    refunds = [
        row
        for row in client.get(f"/members/{member['id']}/tokens", headers=AUTH).json()
        if row["kind"] == "booking_refund"
    ]
    assert refunds[0]["meta"]["override"]["reason"] == REASON["reason"]
