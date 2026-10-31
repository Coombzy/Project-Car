"""Ben's four bands. Only Peak counts toward the weekly cap.

Off-peak 0.75 every day 21:00-08:00. Normal 1.00 Mon-Fri 08:00-16:00.
Evening 1.25 every day 16:00-21:00. Peak 1.50 Sat-Sun 08:00-16:00.
Each band is one owner-editable row.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from fastapi.testclient import TestClient

from app.shop_time import PRICING_TZ
from tests.conftest import AUTH, create_hoist, create_member, freeze_shop_clock

MONDAY = datetime(2026, 11, 2, 6, 0, tzinfo=PRICING_TZ)


def _at(day: int, hour: int) -> datetime:
    return datetime(2026, 11, day, hour, 0, tzinfo=PRICING_TZ)


def _quote(client: TestClient, member_id: str, start: datetime) -> dict:
    response = client.post(
        "/bookings/quote",
        headers=AUTH,
        json={
            "member_id": member_id,
            "start_at": start.isoformat(),
            "end_at": datetime(start.year, start.month, start.day, start.hour + 1, tzinfo=start.tzinfo).isoformat(),
        },
    )
    assert response.status_code == 200, response.text
    return response.json()


def test_each_hour_uses_one_named_band(client: TestClient) -> None:
    freeze_shop_clock(MONDAY)
    member = create_member(client)
    cases = (
        (_at(7, 10), "weekend_fri_eve", "Peak", "150.00"),
        (_at(7, 16), "weekday_eve", "Evening", "125.00"),
        (_at(7, 21), "late_night", "Off-peak", "75.00"),
        (_at(8, 9), "weekend_fri_eve", "Peak", "150.00"),
        (_at(8, 18), "weekday_eve", "Evening", "125.00"),
        (_at(6, 16), "weekday_eve", "Evening", "125.00"),
        (_at(2, 10), "weekday_day", "Normal", "100.00"),
        (_at(2, 7), "late_night", "Off-peak", "75.00"),
    )
    for start, band_id, label, tokens in cases:
        quoted = _quote(client, member["id"], start)
        rule = quoted["pricing_rule"]
        assert (rule["band_id"], rule["band_label"], quoted["reserved_tokens"]) == (band_id, label, tokens), start

    listed = client.get("/tiers/pricing", headers=AUTH)
    assert listed.status_code == 200, listed.text
    bands = {row["id"]: row for row in listed.json()["bands"]}
    assert bands["late_night"]["label"] == "Off-peak"
    assert bands["weekday_day"]["label"] == "Normal"
    assert bands["weekday_eve"]["label"] == "Evening"
    assert bands["weekend_fri_eve"]["label"] == "Peak"
    assert Decimal(str(bands["weekend_fri_eve"]["multiplier"])) == Decimal("1.50")


def test_only_peak_counts_and_the_owner_can_edit_it(client: TestClient) -> None:
    freeze_shop_clock(MONDAY)
    member = create_member(client)
    hoist = create_hoist(client)
    peak = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": _at(7, 8).isoformat(),
            "end_at": _at(7, 12).isoformat(),
        },
    )
    assert peak.status_code == 201, peak.text
    raised = client.patch(
        "/tiers/premium",
        headers=AUTH,
        json={"max_simultaneous_bookings": 3},
    )
    assert raised.status_code == 200, raised.text
    evening = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": _at(7, 18).isoformat(),
            "end_at": _at(7, 19).isoformat(),
        },
    )
    assert evening.status_code == 201, evening.text
    fifth = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": _at(7, 12).isoformat(),
            "end_at": _at(7, 13).isoformat(),
        },
    )
    assert fifth.status_code == 409, fifth.text
    assert fifth.json()["error"]["code"] == "peak_cap"

    patched = client.patch(
        "/tiers/bands/weekend_fri_eve",
        headers=AUTH,
        json={"multiplier": "1.60"},
    )
    assert patched.status_code == 200, patched.text
    sunday = _quote(client, member["id"], _at(8, 10))
    assert Decimal(str(sunday["pricing_rule"]["band_multiplier"])) == Decimal("1.60")
    assert Decimal(str(sunday["reserved_tokens"])) == Decimal("160.00")
