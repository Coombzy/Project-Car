from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace
from uuid import uuid4

from app.models import BookingKind, BookingStatus
from app.services.hours import booking_overlaps_window, expand_booked_hours
from app.shop_time import PRICING_TZ, next_24h_bounds


def test_naive_local_afternoon_overlaps_utc_window() -> None:
    window_start, window_end = next_24h_bounds(datetime(2026, 9, 6, 14, 45, tzinfo=PRICING_TZ))
    booking = SimpleNamespace(
        status=BookingStatus.CONFIRMED,
        start_at=datetime(2026, 9, 6, 16, 0, 0),
        end_at=datetime(2026, 9, 6, 18, 0, 0),
    )
    assert booking_overlaps_window(booking, window_start, window_end)
    # Naive SQL against a UTC bound would drop this row (18:00 < 20:45Z).
    assert booking.end_at < window_start.replace(tzinfo=None)


def test_expand_booked_hours_keeps_naive_local_seed_slots() -> None:
    now = datetime(2026, 9, 6, 14, 45, tzinfo=PRICING_TZ)
    window_start, window_end = next_24h_bounds(now)
    hoist_id = uuid4()
    booking = SimpleNamespace(
        id=uuid4(),
        hoist_id=hoist_id,
        hoist=SimpleNamespace(name="Bay 1"),
        member_id=uuid4(),
        member=SimpleNamespace(name="Ada Reyes"),
        kind=BookingKind.CUSTOMER,
        status=BookingStatus.CONFIRMED,
        start_at=datetime(2026, 9, 6, 16, 0, 0),
        end_at=datetime(2026, 9, 6, 18, 0, 0),
        notes="1992 Miata — turbo mock-up",
    )
    hours = expand_booked_hours([booking], window_start, window_end)
    assert len(hours) == 2
    assert hours[0]["member_name"] == "Ada Reyes"
    assert hours[0]["vehicle_label"] == "1992 Miata — turbo mock-up"
    assert hours[0]["hour_start"] < hours[1]["hour_start"]


def test_past_naive_morning_slot_is_outside_afternoon_window() -> None:
    window_start, window_end = next_24h_bounds(datetime(2026, 9, 6, 14, 45, tzinfo=PRICING_TZ))
    booking = SimpleNamespace(
        status=BookingStatus.CONFIRMED,
        start_at=datetime(2026, 9, 6, 9, 0, 0),
        end_at=datetime(2026, 9, 6, 11, 0, 0),
    )
    assert booking_overlaps_window(booking, window_start, window_end) is False
    assert (
        expand_booked_hours(
            [
                SimpleNamespace(
                    id=uuid4(),
                    hoist_id=uuid4(),
                    hoist=SimpleNamespace(name="Bay 2"),
                    member_id=uuid4(),
                    member=SimpleNamespace(name="Riley Park"),
                    kind=BookingKind.CUSTOMER,
                    status=booking.status,
                    start_at=booking.start_at,
                    end_at=booking.end_at,
                    notes="On the clock",
                )
            ],
            window_start,
            window_end,
        )
        == []
    )
