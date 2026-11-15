"""GET /staff/schedule is windowed and capped (PC-new-1).

The default window is America/Regina today-1 through today+14, and the
default limit is 200. On main the route returns every booking and ignores
limit, so this test fails there.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal
from uuid import UUID

from fastapi.testclient import TestClient

from app.models import Booking, BookingKind, BookingStatus
from app.shop_time import PRICING_TZ, as_utc, pricing_today
from tests.conftest import AUTH, create_hoist, create_member

HOURLY_ROWS = 205


def _regina(day, hour: int = 10) -> datetime:
    """10:00 America/Regina on ``day``, stored as UTC."""
    local = datetime(day.year, day.month, day.day, hour, tzinfo=PRICING_TZ)
    return as_utc(local)


def _booking(member_id: UUID, hoist_id: UUID, start: datetime) -> Booking:
    return Booking(
        member_id=member_id,
        hoist_id=hoist_id,
        start_at=start,
        end_at=as_utc(start + timedelta(hours=1)),
        kind=BookingKind.CUSTOMER,
        status=BookingStatus.CONFIRMED,
        reserved_tokens=Decimal("0"),
    )


def test_staff_schedule_is_windowed_and_capped(client: TestClient) -> None:
    member = create_member(
        client, email="sched-window@example.com", allocate_tokens=False
    )
    hoist = create_hoist(client, name="Schedule bay")
    today = pricing_today()
    member_id = UUID(member["id"])
    hoist_id = UUID(hoist["id"])

    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        old = _booking(member_id, hoist_id, _regina(today - timedelta(days=60)))
        tomorrow = _booking(member_id, hoist_id, _regina(today + timedelta(days=1)))
        session.add(old)
        session.add(tomorrow)
        # Hourly, not daily: 205 days would leave the today+14 window.
        first = _regina(today + timedelta(days=2))
        for index in range(HOURLY_ROWS):
            session.add(
                _booking(member_id, hoist_id, as_utc(first + timedelta(hours=index)))
            )
        session.commit()
        old_id = str(old.id)
        tomorrow_id = str(tomorrow.id)
    finally:
        session.close()

    schedule = client.get("/staff/schedule", headers=AUTH)
    assert schedule.status_code == 200, schedule.text
    ids = [row["id"] for row in schedule.json()]
    assert len(ids) == 200
    assert tomorrow_id in ids
    assert old_id not in ids

    rejected = client.get("/staff/schedule", headers=AUTH, params={"limit": 0})
    assert rejected.status_code == 422
