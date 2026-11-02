"""Omitting the bay picks the lowest-numbered free member bay. Bay 6 is never that pick.

Docs/token-pricing.md: the saved booking names the bay. A lost hour tries the
next bay in the same save. A visit with no free member bay writes nothing.
"""

from __future__ import annotations

from datetime import timedelta
from decimal import Decimal

from fastapi.testclient import TestClient

from app.shop_time import shop_now
from tests.conftest import AUTH, create_hoist, create_member, login_member


def _window(hours_from_now: int = 8, length_hours: int = 2) -> tuple[str, str]:
    start = shop_now() + timedelta(hours=hours_from_now)
    end = start + timedelta(hours=length_hours)
    return start.isoformat(), end.isoformat()


def _book(client: TestClient, member_id: str, hoist_id: str, start: str, end: str):
    return client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member_id,
            "hoist_id": hoist_id,
            "start_at": start,
            "end_at": end,
        },
    )


def test_omitted_bay_picks_the_lowest_free_member_bay(client: TestClient) -> None:
    member = create_member(client, email="bay-pick@example.com")
    bay1 = create_hoist(client, name="Bay 1")
    bay2 = create_hoist(client, name="Bay 2")
    shop = create_hoist(client, name="Bay 6", location_label="Shop", is_shop=True)
    start, end = _window()
    login_member(client, member["email"])

    created = client.post("/member/bookings", json={"start_at": start, "end_at": end})
    assert created.status_code == 201, created.text
    body = created.json()
    assert body["kind"] == "customer"
    assert body["hoist_id"] == bay1["id"]
    assert body["hoist_name"] == "Bay 1"
    assert body["hoist_id"] != shop["id"]
    assert body["hoist_id"] != bay2["id"]


def test_a_lost_hour_tries_the_next_member_bay(client: TestClient) -> None:
    holder = create_member(client, email="bay-holder@example.com")
    member = create_member(client, email="bay-next@example.com", name="Casey")
    bay1 = create_hoist(client, name="Bay 1")
    bay2 = create_hoist(client, name="Bay 2")
    create_hoist(client, name="Bay 6", location_label="Shop", is_shop=True)
    start, end = _window()
    # One hour of the visit is already on Bay 1. Bay 2 is free for both hours.
    overlap_end = (shop_now() + timedelta(hours=9)).isoformat()
    held = _book(client, holder["id"], bay1["id"], start, overlap_end)
    assert held.status_code == 201, held.text

    login_member(client, member["email"])
    created = client.post("/member/bookings", json={"start_at": start, "end_at": end})
    assert created.status_code == 201, created.text
    assert created.json()["hoist_id"] == bay2["id"]
    assert created.json()["hoist_name"] == "Bay 2"


def test_shop_hoist_is_never_the_automatic_bay(client: TestClient) -> None:
    member = create_member(client, email="bay-shop@example.com", allocate_tokens=False)
    create_hoist(client, name="Bay 6", location_label="Shop", is_shop=True)
    start, end = _window()
    login_member(client, member["email"])
    opening = Decimal(str(client.get("/member/me").json()["token_balance"]))

    refused = client.post("/member/bookings", json={"start_at": start, "end_at": end})
    assert refused.status_code == 409, refused.text
    assert refused.json()["error"]["code"] == "no_free_bay"
    assert client.get("/member/bookings").json() == []
    assert Decimal(str(client.get("/member/me").json()["token_balance"])) == opening


def test_maintenance_bay_is_skipped_for_the_next_free_number(client: TestClient) -> None:
    member = create_member(client, email="bay-maint@example.com")
    bay1 = create_hoist(client, name="Bay 1")
    bay2 = create_hoist(client, name="Bay 2")
    locked = client.patch(
        f"/hoists/{bay1['id']}",
        headers=AUTH,
        json={"status": "maintenance"},
    )
    assert locked.status_code == 200, locked.text
    start, end = _window()
    login_member(client, member["email"])

    created = client.post("/member/bookings", json={"start_at": start, "end_at": end})
    assert created.status_code == 201, created.text
    assert created.json()["hoist_id"] == bay2["id"]


def test_lowest_number_wins_over_name_order(client: TestClient) -> None:
    member = create_member(client, email="bay-order@example.com")
    create_hoist(client, name="Bay 10")
    bay2 = create_hoist(client, name="Bay 2")
    start, end = _window()

    created = client.post(
        "/bookings",
        headers=AUTH,
        json={"member_id": member["id"], "start_at": start, "end_at": end},
    )
    assert created.status_code == 201, created.text
    assert created.json()["hoist_id"] == bay2["id"]
    assert created.json()["hoist_name"] == "Bay 2"
