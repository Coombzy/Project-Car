from __future__ import annotations

from datetime import datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal

from fastapi.testclient import TestClient

from app.services.pricing import FillFactor, quote_reserve
from app.shop_time import PRICING_TZ, shop_now
from tests.conftest import AUTH


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


def test_fill_factor_stacks_on_band_and_overlay() -> None:
    start = _at(2026, 9, 8, 17)
    end = start + timedelta(hours=2)
    reserved_at = start - timedelta(hours=30)
    fill = FillFactor(
        id="next_day_open",
        label="Fill the gaps 25%",
        multiplier=Decimal("0.75"),
        discount_pct=Decimal("25"),
    )
    quote = quote_reserve(start, end, reserved_at=reserved_at, fill=fill)
    assert quote.band.multiplier == Decimal("1.25")
    assert quote.overlay.multiplier == Decimal("1.25")
    assert quote.fill.multiplier == Decimal("0.75")
    assert quote.final_reserve_cost == Decimal("234.38")
    rule = quote.as_rule()
    assert rule["fill_multiplier"] == "0.75"
    assert rule["fill_discount_pct"] == "25"
    assert rule["advance_multiplier"] == "1.25"
    unchanged = quote_reserve(start, end, reserved_at=reserved_at)
    assert unchanged.final_reserve_cost == Decimal("312.50")
    assert unchanged.fill.id == "none"


def _weekday_day_in_standard_window() -> datetime:
    """A future Mon–Fri 10:00 whose overlay is standard (48h–7d ahead)."""
    now = shop_now().astimezone(PRICING_TZ)
    for ahead in range(2, 7):
        start = (now + timedelta(days=ahead)).replace(hour=10, minute=0, second=0, microsecond=0)
        if start.weekday() >= 5:
            continue
        delta = start - now
        if timedelta(hours=48) <= delta < timedelta(days=7):
            return start
    raise AssertionError("no weekday-day slot inside the standard overlay window")


def test_owner_can_patch_band_multiplier_and_quote_uses_it(client: TestClient) -> None:
    denied = client.patch("/tiers/bands/weekday_day", json={"multiplier": "1.10"})
    assert denied.status_code == 401

    patched = client.patch(
        "/tiers/bands/weekday_day",
        headers=AUTH,
        json={"multiplier": "1.10"},
    )
    assert patched.status_code == 200, patched.text
    body = patched.json()
    assert body["id"] == "weekday_day"
    assert Decimal(str(body["multiplier"])) == Decimal("1.10")

    start = _weekday_day_in_standard_window()
    end = start + timedelta(hours=1)
    quoted = client.post(
        "/bookings/quote",
        headers=AUTH,
        json={"start_at": start.isoformat(), "end_at": end.isoformat()},
    )
    assert quoted.status_code == 200, quoted.text
    rule = quoted.json()["pricing_rule"]
    assert rule["band_id"] == "weekday_day"
    assert rule["overlay_id"] == "standard"
    assert Decimal(str(rule["band_multiplier"])) == Decimal("1.10")
    assert Decimal(str(quoted.json()["reserved_tokens"])) == Decimal("110.00")
    constant = quote_reserve(start, end, reserved_at=start - timedelta(hours=72))
    assert constant.band.multiplier == Decimal("1.00")
    assert constant.final_reserve_cost == Decimal("100.00")

    overlay = client.patch(
        "/tiers/overlays/standard",
        headers=AUTH,
        json={"multiplier": "0.90"},
    )
    assert overlay.status_code == 200, overlay.text
    assert Decimal(str(overlay.json()["multiplier"])) == Decimal("0.90")
    requoted = client.post(
        "/bookings/quote",
        headers=AUTH,
        json={"start_at": start.isoformat(), "end_at": end.isoformat()},
    )
    assert requoted.status_code == 200, requoted.text
    assert Decimal(str(requoted.json()["reserved_tokens"])) == Decimal("99.00")


def test_invalid_overlay_does_not_commit_a_valid_band(client: TestClient) -> None:
    """One save with a valid band and an invalid overlay must change no multiplier row."""
    patched = client.patch(
        "/tiers/pricing",
        headers=AUTH,
        json={
            "bands": [{"id": "weekday_day", "multiplier": "1.10"}],
            "overlays": [{"id": "standard", "multiplier": "0"}],
        },
    )
    assert patched.status_code == 422, patched.text

    listed = client.get("/tiers/pricing", headers=AUTH)
    assert listed.status_code == 200, listed.text
    bands = {row["id"]: Decimal(str(row["multiplier"])) for row in listed.json()["bands"]}
    assert bands["weekday_day"] == Decimal("1.00")

    start = _weekday_day_in_standard_window()
    end = start + timedelta(hours=1)
    quoted = client.post(
        "/bookings/quote",
        headers=AUTH,
        json={"start_at": start.isoformat(), "end_at": end.isoformat()},
    )
    assert quoted.status_code == 200, quoted.text
    rule = quoted.json()["pricing_rule"]
    assert rule["band_id"] == "weekday_day"
    assert rule["overlay_id"] == "standard"
    assert Decimal(str(rule["band_multiplier"])) == Decimal("1.00")
    assert Decimal(str(quoted.json()["reserved_tokens"])) == Decimal("100.00")


def test_owner_can_patch_band_and_overlay_in_one_request(client: TestClient) -> None:
    patched = client.patch(
        "/tiers/pricing",
        headers=AUTH,
        json={
            "bands": [{"id": "weekday_day", "multiplier": "1.10"}],
            "overlays": [{"id": "standard", "multiplier": "0.90"}],
        },
    )
    assert patched.status_code == 200, patched.text
    body = patched.json()
    bands = {row["id"]: Decimal(str(row["multiplier"])) for row in body["bands"]}
    overlays = {row["id"]: Decimal(str(row["multiplier"])) for row in body["overlays"]}
    assert bands["weekday_day"] == Decimal("1.10")
    assert overlays["standard"] == Decimal("0.90")

    start = _weekday_day_in_standard_window()
    end = start + timedelta(hours=1)
    quoted = client.post(
        "/bookings/quote",
        headers=AUTH,
        json={"start_at": start.isoformat(), "end_at": end.isoformat()},
    )
    assert quoted.status_code == 200, quoted.text
    assert Decimal(str(quoted.json()["reserved_tokens"])) == Decimal("99.00")


def test_per_hour_band_audit_case() -> None:
    """Monday, reserved 8 days ahead. Adding the 07:00 hour must not get cheaper."""
    reserved_at = _at(2026, 9, 7, 7) - timedelta(days=8)
    from_seven = quote_reserve(
        _at(2026, 9, 7, 7),
        _at(2026, 9, 7, 21),
        reserved_at=reserved_at,
    )
    from_eight = quote_reserve(
        _at(2026, 9, 7, 8),
        _at(2026, 9, 7, 21),
        reserved_at=reserved_at,
    )
    assert from_seven.overlay.id == "advance"
    assert from_eight.overlay.id == "advance"
    # (1×0.75 + 8×1.00 + 5×1.25) × 100 × 0.85
    assert from_seven.final_reserve_cost == Decimal("1275.00")
    # 14.25 × 85
    assert from_eight.final_reserve_cost == Decimal("1211.25")
    assert from_seven.final_reserve_cost > from_eight.final_reserve_cost
    assert from_seven.band.id == "late_night"
    assert from_eight.band.id == "weekday_day"
    assert [segment.band.id for segment in from_seven.segments] == [
        "late_night",
        "weekday_day",
        "weekday_eve",
    ]


def test_partial_hour_prorates_across_a_boundary() -> None:
    start = _at(2026, 9, 7, 7, 30)
    end = _at(2026, 9, 7, 8, 30)
    quote = quote_reserve(start, end, reserved_at=start - timedelta(hours=72))
    assert quote.overlay.id == "standard"
    # 0.5×0.75 + 0.5×1.00, × 100
    assert quote.final_reserve_cost == Decimal("87.50")
    assert len(quote.segments) == 2
    assert quote.segments[0].hours == Decimal("0.5")
    assert quote.segments[1].hours == Decimal("0.5")


def test_extending_by_an_hour_never_costs_less() -> None:
    days = (
        _at(2026, 9, 7, 0),  # Monday
        _at(2026, 9, 11, 0),  # Friday
        _at(2026, 9, 12, 0),  # Saturday
        _at(2026, 9, 13, 0),  # Sunday
    )
    for day in days:
        for hour in range(24):
            start = day + timedelta(hours=hour)
            reserved_at = start - timedelta(days=8)
            for length in range(1, 24):
                shorter = quote_reserve(
                    start,
                    start + timedelta(hours=length),
                    reserved_at=reserved_at,
                )
                longer = quote_reserve(
                    start,
                    start + timedelta(hours=length + 1),
                    reserved_at=reserved_at,
                )
                assert longer.final_reserve_cost >= shorter.final_reserve_cost, (
                    f"{start.isoformat()} length {length}: "
                    f"{shorter.final_reserve_cost} -> {longer.final_reserve_cost}"
                )


def test_booking_across_midnight_splits_at_midnight() -> None:
    start = _at(2026, 9, 7, 20)  # Monday 20:00
    end = _at(2026, 9, 8, 2)  # Tuesday 02:00
    quote = quote_reserve(start, end, reserved_at=start - timedelta(hours=72))
    assert quote.overlay.id == "standard"
    # 1×1.25 + 5×0.75, × 100
    assert quote.final_reserve_cost == Decimal("500.00")
    assert len(quote.segments) == 2
    eve, late = quote.segments
    assert eve.band.id == "weekday_eve"
    assert eve.hours == Decimal("1")
    assert late.band.id == "late_night"
    assert late.hours == Decimal("5")
    assert late.start.astimezone(PRICING_TZ).hour == 21
    assert late.end.astimezone(PRICING_TZ) == end


def test_us_dst_change_does_not_shift_bands() -> None:
    """2026-11-01 00:00–04:00 America/Regina stays 4.0000h.

    That night US/Canada clocks fall back. Regina does not. Segment edges
    follow PRICING_TZ wall clock, so the span is four hours at UTC−6, not
    five. Sunday 00:00–21:00 is weekend_fri_eve on the locked band table
    (late_night starts at 21:00). The row text says "late-night"; the table
    in Docs/token-pricing.md and resolve_band win.
    """
    start = _at(2026, 11, 1, 0)
    end = _at(2026, 11, 1, 4)
    quote = quote_reserve(start, end, reserved_at=start - timedelta(hours=72))
    assert quote.hours == Decimal("4.0000")
    assert len(quote.segments) == 1
    segment = quote.segments[0]
    assert segment.band.id == "weekend_fri_eve"
    assert segment.hours == Decimal("4.0000")
    assert segment.start.utcoffset() == timedelta(hours=-6)
    assert segment.end.utcoffset() == timedelta(hours=-6)
    assert segment.end - segment.start == timedelta(hours=4)
    assert quote.band.id == "weekend_fri_eve"


def test_fill_applies_to_every_segment() -> None:
    start = _at(2026, 9, 7, 15)  # Monday 15:00
    end = _at(2026, 9, 7, 17)
    fill = FillFactor(
        id="next_day_open",
        label="Fill the gaps 20%",
        multiplier=Decimal("0.80"),
        discount_pct=Decimal("20"),
    )
    quote = quote_reserve(start, end, reserved_at=start - timedelta(hours=72), fill=fill)
    assert quote.overlay.id == "standard"
    # (1×1.00 + 1×1.25) × 100 × 0.80
    assert quote.final_reserve_cost == Decimal("180.00")
    assert [segment.band.id for segment in quote.segments] == ["weekday_day", "weekday_eve"]
    assert quote.segments[0].tokens == Decimal("80")
    assert quote.segments[1].tokens == Decimal("100")


def test_single_band_booking_unchanged() -> None:
    start = _at(2026, 9, 8, 9)  # Tuesday 09:00
    end = _at(2026, 9, 8, 11)
    quote = quote_reserve(start, end, reserved_at=start - timedelta(hours=72))
    assert quote.hours == Decimal("2")
    assert quote.band.id == "weekday_day"
    assert quote.band.multiplier == Decimal("1.00")
    assert quote.overlay.id == "standard"
    assert quote.base_tokens == Decimal("200.00")
    assert quote.final_reserve_cost == Decimal("200.00")
    assert len(quote.segments) == 1
    assert quote.segments[0].band.id == "weekday_day"
    assert quote.segments[0].hours == Decimal("2")
    rule = quote.as_rule()
    assert rule["band_id"] == "weekday_day"
    assert rule["band_multiplier"] == "1"
    assert rule["final_reserve_cost"] == "200.00"


def test_segments_in_rule() -> None:
    start = _at(2026, 9, 8, 17)  # Tuesday 17:00, one band, product needs a final round
    end = start + timedelta(hours=2)
    fill = FillFactor(
        id="next_day_open",
        label="Fill the gaps 25%",
        multiplier=Decimal("0.75"),
        discount_pct=Decimal("25"),
    )
    quote = quote_reserve(start, end, reserved_at=start - timedelta(hours=30), fill=fill)
    rule = quote.as_rule()
    segments = rule["segments"]
    assert isinstance(segments, list) and len(segments) == 1
    hours = sum((Decimal(segment["hours"]) for segment in segments), Decimal("0"))
    tokens = sum((Decimal(segment["tokens"]) for segment in segments), Decimal("0"))
    assert hours == quote.hours
    assert tokens == Decimal("234.375")
    assert tokens.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) == quote.final_reserve_cost
    assert tokens != quote.final_reserve_cost
    assert rule["final_reserve_cost"] == "234.38"
    assert rule["band_id"] == "weekday_eve"

    spanning = quote_reserve(
        _at(2026, 9, 7, 7),
        _at(2026, 9, 7, 21),
        reserved_at=_at(2026, 9, 7, 7) - timedelta(days=8),
    )
    spanning_rule = spanning.as_rule()
    spanning_segments = spanning_rule["segments"]
    assert isinstance(spanning_segments, list) and len(spanning_segments) == 3
    assert sum((Decimal(segment["hours"]) for segment in spanning_segments), Decimal("0")) == spanning.hours
    unrounded = sum((Decimal(segment["tokens"]) for segment in spanning_segments), Decimal("0"))
    assert unrounded.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) == spanning.final_reserve_cost
    assert spanning_rule["band_id"] == spanning.segments[0].band.id
