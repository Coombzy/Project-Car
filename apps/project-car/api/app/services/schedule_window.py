"""Schedule window resolution for booking/pickup windows."""

from __future__ import annotations

from datetime import date, datetime, time, timedelta

from app.shop_time import PRICING_TZ, as_utc

SCHEDULE_PAST_DAYS = 1
SCHEDULE_FUTURE_DAYS = 14


def resolve_schedule_window(
    window_start: date | None,
    window_end: date | None,
    *,
    today: date,
) -> tuple[datetime, datetime]:
    """Return a half-open UTC window for schedule lookups.

    A missing ``window_start`` defaults to ``today - SCHEDULE_PAST_DAYS``.
    A missing ``window_end`` defaults to ``today + SCHEDULE_FUTURE_DAYS``.

    The returned pair is the half-open interval
    ``[start_day 00:00 Regina, day_after_end 00:00 Regina)`` converted to UTC.
    """
    start = window_start or (today - timedelta(days=SCHEDULE_PAST_DAYS))
    end = window_end or (today + timedelta(days=SCHEDULE_FUTURE_DAYS))

    start_dt = datetime.combine(start, time.min, tzinfo=PRICING_TZ)
    end_dt = datetime.combine(end + timedelta(days=1), time.min, tzinfo=PRICING_TZ)

    return as_utc(start_dt), as_utc(end_dt)
