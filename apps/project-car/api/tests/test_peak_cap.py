"""A member cannot hold more than four Peak hours in one shop week.

Peak is Saturday and Sunday 08:00–16:00 America/Regina. Evening does not count.
A booking past the cap is 409 peak_cap and writes no row. Docs/token-pricing.md.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal

from fastapi.testclient import TestClient

from app.shop_time import PRICING_TZ
from tests.conftest import AUTH, create_hoist, create_member, freeze_shop_clock

# Friday 2026-11-06 09:00 Regina. Saturday peak is inside the booking window.
FRIDAY = datetime(2026, 11, 6, 9, 0, tzinfo=PRICING_TZ)
SATURDAY = datetime(2026, 11, 7, tzinfo=PRICING_TZ)


def _book(client: TestClient, member_id: str, hoist_id: str, start: datetime, end: datetime):
    return client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member_id,
            "hoist_id": hoist_id,
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
        },
    )


def _balance(client: TestClient, member_id: str) -> Decimal:
    response = client.get(f"/members/{member_id}", headers=AUTH)
    assert response.status_code == 200, response.text
    return Decimal(str(response.json()["token_balance"]))


def _booking_ids(client: TestClient) -> list[str]:
    response = client.get("/bookings", headers=AUTH)
    assert response.status_code == 200, response.text
    return [row["id"] for row in response.json()]


def test_five_peak_hours_in_one_week_are_refused(client: TestClient) -> None:
    freeze_shop_clock(FRIDAY)
    member = create_member(client, email="peak-cap@example.com", tier_name="premium")
    hoist = create_hoist(client, name="Bay 1")
    opening = _balance(client, member["id"])
    before = _booking_ids(client)

    refused = _book(
        client,
        member["id"],
        hoist["id"],
        SATURDAY.replace(hour=8),
        SATURDAY.replace(hour=13),
    )
    assert refused.status_code == 409, refused.text
    assert refused.json()["error"]["code"] == "peak_cap"
    assert _booking_ids(client) == before
    assert _balance(client, member["id"]) == opening

    held = _book(
        client,
        member["id"],
        hoist["id"],
        SATURDAY.replace(hour=8),
        SATURDAY.replace(hour=12),
    )
    assert held.status_code == 201, held.text
    after_four = _balance(client, member["id"])
    assert after_four < opening

    fifth = _book(
        client,
        member["id"],
        hoist["id"],
        SATURDAY.replace(hour=12),
        SATURDAY.replace(hour=13),
    )
    assert fifth.status_code == 409, fifth.text
    assert fifth.json()["error"]["code"] == "peak_cap"
    assert _balance(client, member["id"]) == after_four
    assert len(_booking_ids(client)) == len(before) + 1

    sunday_evening = datetime(2026, 11, 8, 16, 0, tzinfo=PRICING_TZ)
    evening = _book(
        client,
        member["id"],
        hoist["id"],
        sunday_evening,
        sunday_evening + timedelta(hours=2),
    )
    assert evening.status_code == 201, evening.text

    cancelled = client.post(f"/bookings/{held.json()['id']}/cancel", headers=AUTH)
    assert cancelled.status_code == 200, cancelled.text
    again = _book(
        client,
        member["id"],
        hoist["id"],
        SATURDAY.replace(hour=12),
        SATURDAY.replace(hour=16),
    )
    assert again.status_code == 201, again.text
