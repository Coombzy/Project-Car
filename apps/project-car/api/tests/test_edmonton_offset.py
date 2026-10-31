"""Alberta is permanent UTC-6 from 2026 (IANA tzdata 2026c).

A host whose zoneinfo still has the old Mountain fallback would put
America/Edmonton on UTC-7 at 2026-11-01 02:00. Naive shop times (the Owner
datetime-local clock) would then store an hour late.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import UUID
from zoneinfo import ZoneInfo

import pytest
from fastapi.testclient import TestClient

from app.models import Booking
from app.services.bookings import _stored_utc
from tests.conftest import AUTH, create_hoist, create_member

UTC_MINUS_6 = timedelta(hours=-6)


def test_edmonton_offset_stays_minus_6_after_2026_11_01() -> None:
    edmonton = ZoneInfo("America/Edmonton")
    after_old_fallback = datetime(2026, 11, 1, 3, 0, tzinfo=edmonton)
    mid_december = datetime(2026, 12, 15, 12, 0, tzinfo=edmonton)
    assert after_old_fallback.utcoffset() == UTC_MINUS_6
    assert mid_december.utcoffset() == UTC_MINUS_6


def test_booking_typed_at_10_local_on_2026_11_02_stores_as_16_utc(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """10:00 typed on the shop clock is 16:00 UTC while Edmonton is UTC-6."""
    monkeypatch.setenv("SHOP_NOW", "2026-10-31T09:00:00")
    member = create_member(client)
    hoist = create_hoist(client)
    created = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": "2026-11-02T10:00:00",
            "end_at": "2026-11-02T11:00:00",
        },
    )
    assert created.status_code == 201, created.text

    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        booking = session.get(Booking, UUID(created.json()["id"]))
        assert booking is not None
        stored = _stored_utc(booking.start_at)
    finally:
        session.close()

    assert stored == datetime(2026, 11, 2, 16, 0, tzinfo=timezone.utc)
