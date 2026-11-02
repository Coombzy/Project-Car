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


def _ledger(client: TestClient, member_id: str) -> list[dict]:
    response = client.get(f"/members/{member_id}/tokens", headers=AUTH)
    assert response.status_code == 200, response.text
    return response.json()


def _request(client: TestClient, member_id: str, hoist_id: str, start: datetime, end: datetime):
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


def test_approving_five_peak_hours_on_the_shop_hoist_is_refused(client: TestClient) -> None:
    """Saturday 08:00–13:00 is five Peak hours. Approval must not write a booking."""
    freeze_shop_clock(FRIDAY)
    member = create_member(client, email="shop-peak@example.com", tier_name="premium")
    shop = create_hoist(client, name="Bay 6", is_shop=True)
    opening = _balance(client, member["id"])
    ledger = _ledger(client, member["id"])
    before = _booking_ids(client)

    created = _request(
        client,
        member["id"],
        shop["id"],
        SATURDAY.replace(hour=8),
        SATURDAY.replace(hour=13),
    )
    assert created.status_code == 201, created.text
    assert created.json()["record"] == "shop_hoist_request"
    assert created.json()["status"] == "pending"
    assert _booking_ids(client) == before
    assert _balance(client, member["id"]) == opening

    approved = client.post(f"/shop-hoist-requests/{created.json()['id']}/approve", headers=AUTH)
    assert approved.status_code == 409, approved.text
    assert approved.json()["error"]["code"] == "peak_cap"
    assert _booking_ids(client) == before
    assert _balance(client, member["id"]) == opening
    assert _ledger(client, member["id"]) == ledger
    pending = client.get("/shop-hoist-requests", headers=AUTH, params={"status": "pending"}).json()
    row = next(item for item in pending if item["id"] == created.json()["id"])
    assert row["status"] == "pending"
    assert row["booking_id"] is None


def test_approving_a_fifth_peak_hour_on_bay_6_is_refused(client: TestClient) -> None:
    """Four Peak hours on a member bay plus one more on Bay 6 stays under the cap only if approval checks it."""
    freeze_shop_clock(FRIDAY)
    member = create_member(client, email="shop-fifth@example.com", tier_name="premium")
    bay = create_hoist(client, name="Bay 1")
    shop = create_hoist(client, name="Bay 6", is_shop=True)
    held = _book(
        client,
        member["id"],
        bay["id"],
        SATURDAY.replace(hour=8),
        SATURDAY.replace(hour=12),
    )
    assert held.status_code == 201, held.text
    after_four = _balance(client, member["id"])
    ledger = _ledger(client, member["id"])
    before = _booking_ids(client)

    created = _request(
        client,
        member["id"],
        shop["id"],
        SATURDAY.replace(hour=12),
        SATURDAY.replace(hour=13),
    )
    assert created.status_code == 201, created.text
    assert created.json()["status"] == "pending"

    approved = client.post(f"/shop-hoist-requests/{created.json()['id']}/approve", headers=AUTH)
    assert approved.status_code == 409, approved.text
    assert approved.json()["error"]["code"] == "peak_cap"
    assert _booking_ids(client) == before
    assert _balance(client, member["id"]) == after_four
    assert _ledger(client, member["id"]) == ledger
    shop_rows = client.get("/bookings", headers=AUTH, params={"hoist_id": shop["id"]}).json()
    assert shop_rows == []
