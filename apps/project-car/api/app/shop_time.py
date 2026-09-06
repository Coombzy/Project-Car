"""Shop-local time helpers. The shop is Calgary / Northern Alberta.

Display and naive datetimes (Owner `datetime-local`, `as_utc`, week bounds)
stay on `SHOP_TZ` = America/Edmonton so existing schedule labels stay honest.

Token pricing bands and the advance overlay use `PRICING_TZ` = America/Regina
(`Docs/token-pricing.md`). During Mountain Daylight both zones are UTC−6, so
clock times match. In winter Edmonton is UTC−7 and Regina stays UTC−6 — band
lookup uses the Regina wall clock of the stored UTC instant.
"""

from __future__ import annotations

from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

SHOP_TZ = ZoneInfo("America/Edmonton")
PRICING_TZ = ZoneInfo("America/Regina")


def as_utc(value: datetime) -> datetime:
    """Treat naive datetimes as shop-local, then return UTC."""
    if value.tzinfo is None:
        value = value.replace(tzinfo=SHOP_TZ)
    return value.astimezone(timezone.utc)


def shop_now() -> datetime:
    return datetime.now(SHOP_TZ)


def shop_today() -> date:
    return shop_now().date()


def pricing_now() -> datetime:
    """Wall clock for fill / band-adjacent calendar math (America/Regina)."""
    return datetime.now(PRICING_TZ)


def pricing_today() -> date:
    return pricing_now().date()


def pricing_next_day(now: datetime | None = None) -> date:
    current = (now or pricing_now()).astimezone(PRICING_TZ)
    return current.date() + timedelta(days=1)


def next_24h_bounds(now: datetime | None = None) -> tuple[datetime, datetime]:
    """Half-open [now, now+24h) window in America/Regina, returned in UTC."""
    current = (now or pricing_now()).astimezone(PRICING_TZ)
    end = current + timedelta(hours=24)
    return as_utc(current), as_utc(end)


def iter_regina_hours(start: datetime, end: datetime) -> list[tuple[datetime, datetime]]:
    """Whole Regina clock hours that overlap [start, end)."""
    local_start = as_utc(start).astimezone(PRICING_TZ)
    local_end = as_utc(end).astimezone(PRICING_TZ)
    if local_end <= local_start:
        return []
    hour = local_start.replace(minute=0, second=0, microsecond=0)
    slots: list[tuple[datetime, datetime]] = []
    while hour < local_end:
        nxt = hour + timedelta(hours=1)
        slots.append((as_utc(hour), as_utc(nxt)))
        hour = nxt
    return slots


def day_bounds(day: date) -> tuple[datetime, datetime]:
    start = datetime.combine(day, time.min, tzinfo=SHOP_TZ)
    end = start + timedelta(days=1)
    return start.astimezone(timezone.utc), end.astimezone(timezone.utc)


def pricing_clock_window(
    day: date,
    start_clock: time,
    end_clock: time,
) -> tuple[datetime, datetime]:
    """Half-open [start, end) window on a Regina calendar day, returned in UTC."""
    start = datetime.combine(day, start_clock, tzinfo=PRICING_TZ)
    end = datetime.combine(day, end_clock, tzinfo=PRICING_TZ)
    if end <= start:
        raise ValueError("Fill window end must be after start.")
    return as_utc(start), as_utc(end)


def week_monday(day: date | None = None) -> date:
    current = day or shop_today()
    return current - timedelta(days=current.weekday())
