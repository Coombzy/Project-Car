"""Expand bookings into booked hours for the next 24h dashboard strips."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from app.models import Booking, BookingKind, BookingStatus
from app.shop_time import as_utc, iter_regina_hours

NO_VEHICLE = "No vehicle on file"
OPEN_HOUR_STATUSES = (
    BookingStatus.PENDING,
    BookingStatus.CONFIRMED,
    BookingStatus.ACTIVE,
    BookingStatus.OVERDUE,
)


def booking_vehicle_label(booking: Booking) -> str:
    """Vehicle if the row ever grows one; otherwise notes or a placeholder."""
    vehicle = getattr(booking, "vehicle", None)
    if vehicle:
        label = getattr(vehicle, "label", None) or getattr(vehicle, "name", None) or str(vehicle)
        if str(label).strip():
            return str(label).strip()
    notes = (booking.notes or "").strip()
    return notes or NO_VEHICLE


def booking_member_name(booking: Booking) -> str:
    member = getattr(booking, "member", None)
    if member is not None:
        return member.name
    return "Shop"


def booking_overlaps_window(booking: Booking, window_start: datetime, window_end: datetime) -> bool:
    """True when a booking overlaps [window_start, window_end) after tz normalize.

    SQLite demo rows are often naive shop-local wall clocks; Postgres stores
    aware UTC. Always compare through ``as_utc`` so afternoon Regina slots are
    not dropped against a UTC SQL bound.
    """
    if booking.status not in OPEN_HOUR_STATUSES:
        return False
    return as_utc(booking.start_at) < as_utc(window_end) and as_utc(booking.end_at) > as_utc(
        window_start
    )


def expand_booked_hours(
    bookings: list[Booking],
    window_start: datetime,
    window_end: datetime,
    *,
    hoist_id: UUID | None = None,
    member_id: UUID | None = None,
) -> list[dict]:
    """One row per booked Regina hour in the window."""
    hours: list[dict] = []
    for booking in bookings:
        if not booking_overlaps_window(booking, window_start, window_end):
            continue
        if hoist_id is not None and booking.hoist_id != hoist_id:
            continue
        if member_id is not None and booking.member_id != member_id:
            continue
        overlap_start = max(as_utc(booking.start_at), as_utc(window_start))
        overlap_end = min(as_utc(booking.end_at), as_utc(window_end))
        if overlap_end <= overlap_start:
            continue
        hoist = getattr(booking, "hoist", None)
        for hour_start, hour_end in iter_regina_hours(overlap_start, overlap_end):
            hours.append(
                {
                    "booking_id": booking.id,
                    "hoist_id": booking.hoist_id,
                    "hoist_name": hoist.name if hoist is not None else "Unknown hoist",
                    "kind": booking.kind if isinstance(booking.kind, BookingKind) else BookingKind(booking.kind),
                    "status": booking.status,
                    "hour_start": hour_start,
                    "hour_end": hour_end,
                    "member_id": booking.member_id,
                    "member_name": booking_member_name(booking),
                    "vehicle_label": booking_vehicle_label(booking),
                    "notes": booking.notes,
                }
            )
    hours.sort(key=lambda row: (row["hoist_name"], row["hour_start"], row["member_name"]))
    return hours
