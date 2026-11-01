"""Member cancel windows and no-shows (Ben, D3 / D4 / D5).

- A member cancel at least ``FREE_CANCEL_HOURS`` (24) before the start returns
  the whole reserve. Inside that window the shop keeps
  ``LATE_CANCEL_KEEP_PCT`` (50%) and refunds the rest in one refund row.
- A member cannot cancel at or after the start: 400 ``cancel_after_start``.
- Owner cancels (and bay closures) waive the late fee.
- ``POST /bookings/sweep-no-shows`` marks confirmed bookings that ended without
  a check-in as ``no_show``, keeps ``NO_SHOW_KEEP_PCT`` (100%) of the reserve
  and frees their hours. Repeat sweeps change nothing.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete, select

from app.models import Booking, BookingHour, StaffAction
from app.services import bookings as booking_service
from app.shop_time import as_utc
from tests.conftest import (
    AUTH,
    create_hoist,
    create_member,
    freeze_shop_clock,
    login_member,
    next_hour,
)

AI = {"Authorization": "Bearer dev-ai-secret"}


def _member_booking(client: TestClient, *, hours_ahead: int = 30, length: int = 2) -> tuple[dict, dict, datetime]:
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
    confirmed = client.post(f"/member/bookings/{created.json()['id']}/confirm")
    assert confirmed.status_code == 200, confirmed.text
    return member, confirmed.json(), start


def _balance(client: TestClient, member_id: str) -> Decimal:
    return Decimal(str(client.get(f"/members/{member_id}", headers=AUTH).json()["token_balance"]))


def _refunds(client: TestClient, member_id: str) -> list[dict]:
    rows = client.get(f"/members/{member_id}/tokens", headers=AUTH).json()
    return [row for row in rows if row["kind"] == "booking_refund"]


def _booking(client: TestClient, booking_id: str) -> dict:
    return next(row for row in client.get("/bookings", headers=AUTH).json() if row["id"] == booking_id)


def _held_hours(client: TestClient, booking_id: str) -> int:
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        return len(session.scalars(select(BookingHour).where(BookingHour.booking_id == UUID(booking_id))).all())
    finally:
        session.close()


def _no_show_actions(client: TestClient) -> list[StaffAction]:
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        return list(session.scalars(select(StaffAction).where(StaffAction.action == "no_show")).all())
    finally:
        session.close()


def test_member_cancel_24h_or_more_ahead_refunds_everything(client: TestClient) -> None:
    member, booking, start = _member_booking(client)
    freeze_shop_clock(start - timedelta(hours=booking_service.FREE_CANCEL_HOURS))
    before = _balance(client, member["id"])
    reserved = Decimal(booking["reserved_tokens"])

    cancelled = client.post(f"/member/bookings/{booking['id']}/cancel")

    assert cancelled.status_code == 200, cancelled.text
    assert cancelled.json()["status"] == "cancelled"
    assert _balance(client, member["id"]) == before + reserved
    [refund] = _refunds(client, member["id"])
    assert Decimal(refund["amount"]) == reserved
    assert refund["meta"]["policy"] == "free_cancel"


def test_member_cancel_inside_24h_keeps_half(client: TestClient) -> None:
    member, booking, start = _member_booking(client)
    freeze_shop_clock(start - timedelta(hours=10))
    before = _balance(client, member["id"])
    reserved = Decimal(booking["reserved_tokens"])
    kept = (reserved / 2).quantize(Decimal("0.01"))

    cancelled = client.post(f"/member/bookings/{booking['id']}/cancel")

    assert cancelled.status_code == 200, cancelled.text
    assert Decimal(cancelled.json()["reserved_tokens"]) == 0
    assert _balance(client, member["id"]) == before + reserved - kept
    [refund] = _refunds(client, member["id"])
    assert Decimal(refund["amount"]) == reserved - kept
    assert refund["meta"]["policy"] == "late_cancel"
    assert Decimal(refund["meta"]["keep_pct"]) == booking_service.LATE_CANCEL_KEEP_PCT == 50
    assert Decimal(refund["meta"]["kept_tokens"]) == kept
    assert Decimal(refund["meta"]["hours_before"]) == 10
    assert _held_hours(client, booking["id"]) == 0


def test_kept_share_rounds_half_up_to_the_cent() -> None:
    assert booking_service.kept_share(Decimal("100.01"), Decimal("50")) == Decimal("50.01")
    assert booking_service.kept_share(Decimal("225"), Decimal("50")) == Decimal("112.50")
    assert booking_service.kept_share(Decimal("80"), Decimal("100")) == Decimal("80.00")
    assert booking_service.kept_share(Decimal("80"), Decimal("0")) == Decimal("0.00")


@pytest.mark.parametrize("after_start", [timedelta(0), timedelta(minutes=1)])
def test_member_cannot_cancel_at_or_after_the_start(client: TestClient, after_start: timedelta) -> None:
    member, booking, start = _member_booking(client)
    freeze_shop_clock(start + after_start)
    before = _balance(client, member["id"])

    refused = client.post(f"/member/bookings/{booking['id']}/cancel")

    assert refused.status_code == 400, refused.text
    assert refused.json()["error"]["code"] == "cancel_after_start"
    assert _booking(client, booking["id"])["status"] == "confirmed"
    assert _balance(client, member["id"]) == before
    assert _refunds(client, member["id"]) == []


def test_owner_cancel_inside_24h_waives_the_fee(client: TestClient) -> None:
    member, booking, start = _member_booking(client)
    freeze_shop_clock(start - timedelta(hours=2))
    before = _balance(client, member["id"])
    reserved = Decimal(booking["reserved_tokens"])

    cancelled = client.post(f"/bookings/{booking['id']}/cancel", headers=AUTH, json={"reason": "Owner cancelled this visit"})

    assert cancelled.status_code == 200, cancelled.text
    assert _balance(client, member["id"]) == before + reserved
    [refund] = _refunds(client, member["id"])
    assert "policy" not in (refund["meta"] or {})


def test_sweep_marks_no_shows_keeps_the_reserve_and_is_idempotent(client: TestClient) -> None:
    member, booking, start = _member_booking(client, length=2)
    freeze_shop_clock(start + timedelta(hours=2))
    before = _balance(client, member["id"])

    swept = client.post("/bookings/sweep-no-shows", headers=AUTH)

    assert swept.status_code == 200, swept.text
    assert [row["id"] for row in swept.json()] == [booking["id"]]
    stored = _booking(client, booking["id"])
    assert stored["status"] == "no_show"
    assert Decimal(stored["reserved_tokens"]) == 0
    assert _balance(client, member["id"]) == before
    assert _refunds(client, member["id"]) == []
    assert _held_hours(client, booking["id"]) == 0
    assert len(_no_show_actions(client)) == 1

    again = client.post("/bookings/sweep-no-shows", headers=AUTH)
    assert again.status_code == 200, again.text
    assert again.json() == []
    assert len(_no_show_actions(client)) == 1
    assert _balance(client, member["id"]) == before


def test_sweep_skips_bookings_that_have_not_ended(client: TestClient) -> None:
    _member, booking, start = _member_booking(client, length=2)
    freeze_shop_clock(start + timedelta(hours=1, minutes=59))

    swept = client.post("/bookings/sweep-no-shows", headers=AUTH)

    assert swept.status_code == 200, swept.text
    assert swept.json() == []
    assert _booking(client, booking["id"])["status"] == "confirmed"


def test_ai_may_sweep_and_no_show_is_final(client: TestClient) -> None:
    _member, booking, start = _member_booking(client, length=1)
    freeze_shop_clock(start + timedelta(hours=1))

    swept = client.post("/bookings/sweep-no-shows", headers=AI)
    assert swept.status_code == 200, swept.text
    assert [row["status"] for row in swept.json()] == ["no_show"]

    for path, headers in (
        (f"/bookings/{booking['id']}/cancel", AUTH),
        (f"/bookings/{booking['id']}/check-in", AUTH),
        (f"/member/bookings/{booking['id']}/cancel", {}),
    ):
        response = client.post(path, headers=headers)
        assert response.status_code == 400, (path, response.text)
    assert _booking(client, booking["id"])["status"] == "no_show"


def test_get_bookings_logs_and_skips_a_holding_hours_conflict(
    client: TestClient, caplog: pytest.LogCaptureFixture
) -> None:
    """GET /bookings logs a sweep conflict and leaves that booking alone."""
    _member, elapsed, start = _member_booking(client, hours_ahead=30, length=1)
    quinn = create_member(client, name="Quinn", email="quinn@example.com", tier_name="premium")
    riley = create_member(client, name="Riley", email="riley@example.com", tier_name="premium")
    bay = create_hoist(client, name="Bay 2")
    shared = start + timedelta(hours=10)
    elsewhere = shared + timedelta(hours=5)
    older = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": quinn["id"],
            "hoist_id": bay["id"],
            "start_at": shared.isoformat(),
            "end_at": (shared + timedelta(hours=2)).isoformat(),
        },
    )
    younger = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": riley["id"],
            "hoist_id": bay["id"],
            "start_at": elsewhere.isoformat(),
            "end_at": (elsewhere + timedelta(hours=2)).isoformat(),
        },
    )
    assert older.status_code == 201, older.text
    assert younger.status_code == 201, younger.text
    older_id = UUID(older.json()["id"])
    younger_id = UUID(younger.json()["id"])

    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        older_row = session.get(Booking, older_id)
        younger_row = session.get(Booking, younger_id)
        assert older_row is not None and younger_row is not None
        session.execute(delete(BookingHour).where(BookingHour.booking_id.in_((older_id, younger_id))))
        older_row.start_at = as_utc(shared)
        older_row.end_at = as_utc(shared + timedelta(hours=2))
        younger_row.start_at = as_utc(shared + timedelta(hours=1))
        younger_row.end_at = as_utc(shared + timedelta(hours=3))
        older_row.created_at = datetime(2020, 1, 1, tzinfo=timezone.utc)
        younger_row.created_at = datetime(2020, 1, 2, tzinfo=timezone.utc)
        session.commit()
    finally:
        session.close()

    freeze_shop_clock(start + timedelta(hours=2))
    with caplog.at_level(logging.WARNING, logger="app.services.bookings"):
        listed = client.get("/bookings", headers=AUTH)

    assert listed.status_code == 200, listed.text
    stored = next(row for row in listed.json() if row["id"] == elapsed["id"])
    assert stored["status"] == "confirmed"
    assert _held_hours(client, elapsed["id"]) == 1
    assert any(
        elapsed["id"] in record.message and "unchanged" in record.message for record in caplog.records
    )


def test_no_show_cannot_be_refunded_through_a_refund_request(client: TestClient) -> None:
    member, booking, start = _member_booking(client, length=1)
    freeze_shop_clock(start + timedelta(hours=1))
    assert client.post("/bookings/sweep-no-shows", headers=AUTH).status_code == 200
    before = _balance(client, member["id"])

    filed = client.post("/refund-requests", headers=AI, json={"booking_id": booking["id"]})

    assert filed.status_code == 409, filed.text
    assert filed.json()["error"]["code"] == "refund_not_open"
    assert _balance(client, member["id"]) == before
