"""Each held hour is priced at its own band; the reserve is the sum of those hours.

Ben's rule (2026-10-30): a booking is charged per hour, each hour at the band
that contains it, and the total is the sum. A longer booking can never cost
less than a shorter one inside it. ``pricing_rule.segments`` lists one entry
per held Regina hour, so quote, create and the ledger all explain the price.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from app.services.pricing import quote_reserve
from app.shop_time import PRICING_TZ
from tests.conftest import AUTH, create_hoist, create_member

# Mon 2026-11-02 09:00 Calgary time, the review's probe clock.
FROZEN_NOW = "2026-11-02T09:00:00-06:00"


def _at(year: int, month: int, day: int, hour: int, minute: int = 0) -> datetime:
    return datetime(year, month, day, hour, minute, tzinfo=PRICING_TZ)


def _standard(start: datetime) -> datetime:
    return start - timedelta(hours=72)


def test_band_crossing_booking_charges_each_hour_at_its_band() -> None:
    thursday_15 = _at(2026, 11, 5, 15)
    thursday_16 = _at(2026, 11, 5, 16)
    thursday_21 = _at(2026, 11, 5, 21)

    six_hours = quote_reserve(thursday_15, thursday_21, reserved_at=_standard(thursday_15))
    five_hours = quote_reserve(thursday_16, thursday_21, reserved_at=_standard(thursday_15))

    # 15:00 is weekday day (100); 16:00-20:00 are weekday evening (5 x 125).
    assert six_hours.final_reserve_cost == Decimal("725.00")
    assert five_hours.final_reserve_cost == Decimal("625.00")
    assert six_hours.final_reserve_cost > five_hours.final_reserve_cost


def test_friday_afternoon_into_evening_is_split_by_band() -> None:
    start = _at(2026, 11, 6, 15)
    quote = quote_reserve(start, start + timedelta(hours=2), reserved_at=_standard(start))
    assert quote.final_reserve_cost == Decimal("250.00")
    rule = quote.as_rule()
    assert [segment["band_id"] for segment in rule["segments"]] == [
        "weekday_day",
        "weekend_fri_eve",
    ]
    assert [segment["band_tokens"] for segment in rule["segments"]] == ["100", "150"]
    assert rule["band_id"] == "mixed"
    assert rule["banded_tokens"] == "250"


def test_reserve_covers_every_held_hour() -> None:
    """A partial-hour span is charged for every whole hour it holds."""
    start = _at(2026, 11, 6, 16, 59)
    end = _at(2026, 11, 6, 17, 1)
    quote = quote_reserve(start, end, reserved_at=_standard(start))
    segments = quote.as_rule()["segments"]
    assert len(segments) == 2
    assert quote.final_reserve_cost == Decimal("300.00")


@pytest.mark.parametrize(
    "ahead",
    [timedelta(hours=1), timedelta(hours=30), timedelta(hours=72), timedelta(days=8)],
)
def test_lead_time_does_not_change_the_price(ahead: timedelta) -> None:
    """D6 + D7: no advance discount and no last-minute surcharge."""
    start = _at(2026, 11, 5, 15)
    end = start + timedelta(hours=2)
    quote = quote_reserve(start, end, reserved_at=start - ahead)
    assert quote.overlay.id == "standard"
    assert quote.final_reserve_cost == Decimal("225.00")


@pytest.fixture
def frozen(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SHOP_NOW", FROZEN_NOW)


def test_quote_and_create_agree_on_the_per_hour_total(client: TestClient, frozen: None) -> None:
    member = create_member(client, email="per-hour@example.com")
    bay = create_hoist(client, name="Bay 1")
    window = {
        "start_at": "2026-11-05T15:00:00-06:00",
        "end_at": "2026-11-05T21:00:00-06:00",
    }

    quoted = client.post("/bookings/quote", headers=AUTH, json={**window, "member_id": member["id"]})
    assert quoted.status_code == 200, quoted.text
    assert Decimal(str(quoted.json()["reserved_tokens"])) == Decimal("725.00")
    assert len(quoted.json()["pricing_rule"]["segments"]) == 6

    created = client.post(
        "/bookings",
        headers=AUTH,
        json={**window, "member_id": member["id"], "hoist_id": bay["id"]},
    )
    assert created.status_code == 201, created.text
    body = created.json()
    assert Decimal(str(body["reserved_tokens"])) == Decimal("725.00")
    assert [segment["band_tokens"] for segment in body["pricing_rule"]["segments"]] == [
        "100",
        "125",
        "125",
        "125",
        "125",
        "125",
    ]

    ledger = client.get(f"/members/{member['id']}/tokens", headers=AUTH).json()
    reserve = next(row for row in ledger if row["kind"] == "booking_reserve")
    assert Decimal(str(reserve["amount"])) == Decimal("-725.00")
    assert len(reserve["meta"]["pricing_rule"]["segments"]) == 6
