"""Shop-local time helpers. The shop is Calgary / Northern Alberta."""

from __future__ import annotations

from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

SHOP_TZ = ZoneInfo("America/Edmonton")


def as_utc(value: datetime) -> datetime:
    """Treat naive datetimes as shop-local, then return UTC."""
    if value.tzinfo is None:
        value = value.replace(tzinfo=SHOP_TZ)
    return value.astimezone(timezone.utc)


def shop_now() -> datetime:
    return datetime.now(SHOP_TZ)


def shop_today() -> date:
    return shop_now().date()


def day_bounds(day: date) -> tuple[datetime, datetime]:
    start = datetime.combine(day, time.min, tzinfo=SHOP_TZ)
    end = start + timedelta(days=1)
    return start.astimezone(timezone.utc), end.astimezone(timezone.utc)


def week_monday(day: date | None = None) -> date:
    current = day or shop_today()
    return current - timedelta(days=current.weekday())
