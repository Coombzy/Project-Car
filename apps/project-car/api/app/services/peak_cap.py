"""Weekly peak-hour cap per member (Ben, D13).

Peak is Saturday and Sunday 08:00-16:00 Mountain Time only. A member may
hold ``PEAK_HOURS_PER_WEEK`` of those hours in each shop week (Monday to
Sunday). Evening, Normal, and Off-peak do not count. Cancelled bookings
do not count.
"""

from __future__ import annotations

import enum
from datetime import date, datetime, timedelta, timezone
from typing import assert_never
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Booking, BookingKind, BookingStatus
from app.services.pricing import resolve_band
from app.shop_time import PRICING_TZ, iter_regina_hours

PEAK_HOURS_PER_WEEK = 4
PEAK_BAND_IDS = frozenset({"weekend_fri_eve"})
COUNTED_STATUSES = (
    BookingStatus.PENDING,
    BookingStatus.CONFIRMED,
    BookingStatus.ACTIVE,
    BookingStatus.OVERDUE,
    BookingStatus.COMPLETED,
    BookingStatus.NO_SHOW,
)


class PeakOverCapPolicy(str, enum.Enum):
    """What a booking past the cap does.

    D13 asks for a hook for a later premium on extra peak hours. That would be a
    new value here plus its branch in ``check_peak_cap``; it is not built.
    """

    REFUSE = "refuse"


PEAK_OVER_CAP_POLICY = PeakOverCapPolicy.REFUSE


def _utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _week_start(hour_start: datetime) -> date:
    local = hour_start.astimezone(PRICING_TZ).date()
    return local - timedelta(days=local.weekday())


def _peak_hours_by_week(start_at: datetime, end_at: datetime) -> dict[date, int]:
    counts: dict[date, int] = {}
    for hour_start, _hour_end in iter_regina_hours(_utc(start_at), _utc(end_at)):
        if resolve_band(hour_start).id in PEAK_BAND_IDS:
            week = _week_start(hour_start)
            counts[week] = counts.get(week, 0) + 1
    return counts


def _week_bounds(week: date) -> tuple[datetime, datetime]:
    start = datetime(week.year, week.month, week.day, tzinfo=PRICING_TZ).astimezone(timezone.utc)
    return start, start + timedelta(days=7)


def _used_in_week(session: Session, member_id: UUID, week: date) -> int:
    start, end = _week_bounds(week)
    rows = session.scalars(
        select(Booking).where(
            Booking.member_id == member_id,
            Booking.kind == BookingKind.CUSTOMER,
            Booking.status.in_(COUNTED_STATUSES),
            Booking.start_at < end,
            Booking.end_at > start,
        )
    ).all()
    return sum(_peak_hours_by_week(row.start_at, row.end_at).get(week, 0) for row in rows)


def check_peak_cap(session: Session, member_id: UUID, start_at: datetime, end_at: datetime) -> None:
    for week, requested in sorted(_peak_hours_by_week(start_at, end_at).items()):
        used = _used_in_week(session, member_id, week)
        if used + requested <= PEAK_HOURS_PER_WEEK:
            continue
        match PEAK_OVER_CAP_POLICY:
            case PeakOverCapPolicy.REFUSE:
                raise HTTPException(
                    status_code=409,
                    detail={
                        "code": "peak_cap",
                        "message": (
                            f"That would be {used + requested} peak hours in the week of "
                            f"{week.isoformat()}; the limit is {PEAK_HOURS_PER_WEEK}."
                        ),
                        "cap": PEAK_HOURS_PER_WEEK,
                        "used": used,
                        "requested": requested,
                        "week_start": week.isoformat(),
                    },
                )
            case _ as unreachable:
                assert_never(unreachable)
