from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal

from app.services.pricing import quote_reserve
from app.shop_time import PRICING_TZ


def _at(year: int, month: int, day: int, hour: int, minute: int = 0) -> datetime:
    return datetime(year, month, day, hour, minute, tzinfo=PRICING_TZ)


def test_one_hour_weekday_day_standard_overlay() -> None:
    start = _at(2026, 9, 8, 10)  # Tuesday 10:00 Regina
    end = start + timedelta(hours=1)
    reserved_at = start - timedelta(hours=72)
    quote = quote_reserve(start, end, reserved_at=reserved_at)
    assert quote.hours == Decimal("1")
    assert quote.base_tokens == Decimal("100.00")
    assert quote.band.id == "weekday_day"
    assert quote.band.multiplier == Decimal("1.00")
    assert quote.overlay.id == "standard"
    assert quote.final_reserve_cost == Decimal("100.00")
    assert quote.as_rule()["tz"] == "America/Regina"
    assert quote.as_rule()["hours"] == "1"
    assert quote.as_rule()["base_tokens"] == "100"


def test_one_hour_premium_weekday_evening() -> None:
    start = _at(2026, 9, 8, 17)  # Tuesday 17:00
    end = start + timedelta(hours=1)
    reserved_at = start - timedelta(hours=72)
    quote = quote_reserve(start, end, reserved_at=reserved_at)
    assert quote.band.id == "weekday_eve"
    assert quote.overlay.id == "standard"
    assert quote.final_reserve_cost == Decimal("125.00")


def test_overlay_on_top_of_premium_band() -> None:
    start = _at(2026, 9, 8, 17)
    end = start + timedelta(hours=2)
    reserved_at = start - timedelta(hours=30)
    quote = quote_reserve(start, end, reserved_at=reserved_at)
    assert quote.hours == Decimal("2")
    assert quote.base_tokens == Decimal("200.00")
    assert quote.band.id == "weekday_eve"
    assert quote.overlay.id == "last_minute"
    assert quote.final_reserve_cost == Decimal("312.50")
    rule = quote.as_rule()
    assert rule["final_reserve_cost"] == "312.50"
    assert rule["advance_multiplier"] == "1.25"


def test_ninety_minutes_is_one_and_a_half_hours() -> None:
    start = _at(2026, 9, 8, 10)
    end = start + timedelta(minutes=90)
    reserved_at = start - timedelta(hours=72)
    quote = quote_reserve(start, end, reserved_at=reserved_at)
    assert quote.hours == Decimal("1.5000")
    assert quote.base_tokens == Decimal("150.00")
    assert quote.band.id == "weekday_day"
    assert quote.final_reserve_cost == Decimal("150.00")
    assert quote.as_rule()["hours"] == "1.5"


def test_friday_evening_uses_weekend_premium_not_weekday_eve() -> None:
    start = _at(2026, 9, 11, 16)  # Friday 16:00
    end = start + timedelta(hours=1)
    reserved_at = start - timedelta(hours=72)
    quote = quote_reserve(start, end, reserved_at=reserved_at)
    assert quote.band.id == "weekend_fri_eve"
    assert quote.final_reserve_cost == Decimal("150.00")


def test_overlay_boundaries_seven_days_and_forty_eight_hours() -> None:
    start = _at(2026, 9, 15, 10)
    end = start + timedelta(hours=1)
    exactly_week = quote_reserve(start, end, reserved_at=start - timedelta(days=7))
    just_under_week = quote_reserve(start, end, reserved_at=start - timedelta(days=7) + timedelta(minutes=1))
    exactly_48 = quote_reserve(start, end, reserved_at=start - timedelta(hours=48))
    just_under_48 = quote_reserve(start, end, reserved_at=start - timedelta(hours=48) + timedelta(minutes=1))
    assert exactly_week.overlay.id == "advance"
    assert exactly_week.final_reserve_cost == Decimal("85.00")
    assert just_under_week.overlay.id == "standard"
    assert exactly_48.overlay.id == "standard"
    assert just_under_48.overlay.id == "last_minute"
    assert just_under_48.final_reserve_cost == Decimal("125.00")
