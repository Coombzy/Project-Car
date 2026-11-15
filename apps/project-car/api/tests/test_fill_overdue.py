"""OVERDUE bookings occupy a bay for fill openings (PC-R115)."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from uuid import UUID

from fastapi.testclient import TestClient

from app.models import Booking, BookingKind, BookingStatus
from app.services.fill import OCCUPYING, occupying_bookings
from app.shop_time import as_utc
from tests.conftest import create_hoist, create_member


def test_occupying_includes_overdue() -> None:
    assert BookingStatus.OVERDUE in OCCUPYING
    assert set(OCCUPYING) >= {
        BookingStatus.PENDING,
        BookingStatus.CONFIRMED,
        BookingStatus.ACTIVE,
        BookingStatus.OVERDUE,
    }


def test_occupying_bookings_returns_overdue_row(client: TestClient) -> None:
    member = create_member(client, name="Overdue Fill", email="overdue-fill@example.com", tier_name="premium")
    hoist = create_hoist(client, name="Bay 3")
    start = as_utc(datetime(2026, 9, 8, 10, tzinfo=timezone.utc))
    end = as_utc(start + timedelta(hours=4))
    window_start = as_utc(datetime(2026, 9, 8, 8, tzinfo=timezone.utc))
    window_end = as_utc(datetime(2026, 9, 8, 21, tzinfo=timezone.utc))

    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        session.add(
            Booking(
                member_id=UUID(member["id"]),
                hoist_id=UUID(hoist["id"]),
                start_at=start,
                end_at=end,
                kind=BookingKind.CUSTOMER,
                status=BookingStatus.OVERDUE,
                reserved_tokens=Decimal("0"),
                notes="overdue-visit",
            )
        )
        session.commit()
    finally:
        session.close()

    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        rows = occupying_bookings(session, [UUID(hoist["id"])], window_start, window_end)
        assert len(rows) == 1
        assert rows[0].status == BookingStatus.OVERDUE
        assert rows[0].notes == "overdue-visit"
    finally:
        session.close()
