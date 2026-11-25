from datetime import date, datetime, time, timedelta

from app.services.schedule_window import (
    SCHEDULE_FUTURE_DAYS,
    SCHEDULE_PAST_DAYS,
    resolve_schedule_window,
)
from app.shop_time import PRICING_TZ, as_utc


def test_missing_bounds_default_past_and_future_days():
    today = date(2026, 11, 24)
    start, end = resolve_schedule_window(None, None, today=today)
    assert SCHEDULE_PAST_DAYS == 1
    assert SCHEDULE_FUTURE_DAYS == 14
    assert start == as_utc(
        datetime.combine(today - timedelta(days=1), time.min, tzinfo=PRICING_TZ)
    )
    assert end == as_utc(
        datetime.combine(today + timedelta(days=15), time.min, tzinfo=PRICING_TZ)
    )


def test_explicit_bounds_are_half_open_regina_midnight_in_utc():
    today = date(2026, 11, 24)
    start, end = resolve_schedule_window(
        date(2026, 11, 20), date(2026, 11, 22), today=today
    )
    assert start == as_utc(
        datetime.combine(date(2026, 11, 20), time.min, tzinfo=PRICING_TZ)
    )
    assert end == as_utc(
        datetime.combine(date(2026, 11, 23), time.min, tzinfo=PRICING_TZ)
    )


def test_window_is_utc_and_excludes_the_end_day():
    today = date(2026, 11, 24)
    start, end = resolve_schedule_window(
        date(2026, 11, 20), date(2026, 11, 22), today=today
    )
    assert start.tzinfo is end.tzinfo is not None
    assert start.utcoffset() == end.utcoffset() == timedelta(0)
    # The last instant inside the window is one microsecond before Regina midnight.
    last = (end - timedelta(microseconds=1)).astimezone(PRICING_TZ)
    assert (last.date(), last.time()) == (date(2026, 11, 22), time(23, 59, 59, 999999))
    assert end.astimezone(PRICING_TZ).time() == time.min
    # One explicit day is a full Regina day long, DST-free zone.
    one_day = resolve_schedule_window(date(2026, 11, 20), date(2026, 11, 20), today=today)
    assert one_day[1] - one_day[0] == timedelta(days=1)
