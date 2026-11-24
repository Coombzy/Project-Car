"""Fill discount applies only to hours inside the next-day window."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from fastapi.testclient import TestClient

from app.shop_time import PRICING_TZ
from tests.conftest import AUTH, create_hoist, create_member

FROZEN = "2026-11-24T12:00:00-06:00"
EXPECTED = Decimal("168.75")


def _regina(hour: int) -> datetime:
    return datetime(2026, 11, 25, hour, tzinfo=PRICING_TZ)


def _quote(client: TestClient, start: datetime, end: datetime, member_id: str) -> dict:
    quoted = client.post(
        "/bookings/quote",
        headers=AUTH,
        json={
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
            "member_id": member_id,
        },
    )
    assert quoted.status_code == 200, quoted.text
    return quoted.json()


def _five_empty_bays(client: TestClient, monkeypatch) -> dict:
    monkeypatch.setenv("SHOP_DEV_MODE", "1")
    monkeypatch.setenv("SHOP_NOW", FROZEN)
    member = create_member(client, email="ada@example.com", tier_name="premium")
    for index in range(1, 6):
        create_hoist(client, name=f"Bay {index}")
    return member


def test_two_hour_quote_equals_sum_of_hourly_quotes(client: TestClient, monkeypatch) -> None:
    member = _five_empty_bays(client, monkeypatch)
    evening = _quote(client, _regina(20), _regina(21), member["id"])
    off_peak = _quote(client, _regina(21), _regina(22), member["id"])
    both = _quote(client, _regina(20), _regina(22), member["id"])
    evening_cost = Decimal(str(evening["reserved_tokens"]))
    off_peak_cost = Decimal(str(off_peak["reserved_tokens"]))
    both_cost = Decimal(str(both["reserved_tokens"]))
    assert evening_cost == Decimal("93.75")
    assert off_peak_cost == Decimal("75.00")
    assert both_cost == evening_cost + off_peak_cost == EXPECTED
    assert both["pricing_rule"]["final_reserve_cost"] == "168.75"


def test_reserve_ledger_row_uses_that_number(client: TestClient, monkeypatch) -> None:
    member = _five_empty_bays(client, monkeypatch)
    hoist = client.get("/hoists", headers=AUTH).json()[0]
    created = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": _regina(20).isoformat(),
            "end_at": _regina(22).isoformat(),
        },
    )
    assert created.status_code == 201, created.text
    assert Decimal(str(created.json()["reserved_tokens"])) == EXPECTED
    ledger = client.get(f"/members/{member['id']}/tokens", headers=AUTH)
    assert ledger.status_code == 200, ledger.text
    reserve = next(row for row in ledger.json() if row["kind"] == "booking_reserve")
    assert reserve["meta"]["pricing_rule"]["final_reserve_cost"] == "168.75"
    assert abs(Decimal(str(reserve["amount"]))) == EXPECTED
