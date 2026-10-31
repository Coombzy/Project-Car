"""Bay 6 requests use the same 4-hour peak cap as a member bay."""

from __future__ import annotations

from datetime import datetime

from fastapi.testclient import TestClient

from app.shop_time import PRICING_TZ
from tests.conftest import AUTH, create_hoist, create_member, freeze_shop_clock, login_member

MONDAY = datetime(2026, 11, 2, 9, 0, tzinfo=PRICING_TZ)


def _at(day: int, hour: int) -> datetime:
    return datetime(2026, 11, day, hour, 0, tzinfo=PRICING_TZ)


def _book(client: TestClient, member: dict, hoist: dict, start: datetime, end: datetime):
    return client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
        },
    )


def _request(client: TestClient, shop: dict, start: datetime, end: datetime):
    return client.post(
        "/member/shop-hoist-requests",
        json={
            "hoist_id": shop["id"],
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
        },
    )


def test_saturday_bay6_request_is_refused_at_the_peak_cap(client: TestClient) -> None:
    freeze_shop_clock(MONDAY)
    member = create_member(client)
    bay = create_hoist(client, name="Bay 1")
    shop = create_hoist(client, name="Bay 6", is_shop=True)
    booked = _book(client, member, bay, _at(7, 10), _at(7, 14))
    assert booked.status_code == 201, booked.text
    login_member(client, member["email"])

    refused = _request(client, shop, _at(7, 15), _at(7, 16))

    assert refused.status_code == 409, refused.text
    assert refused.json()["error"]["code"] == "peak_cap"
    assert client.get("/member/shop-hoist-requests").json() == []


def test_approval_takes_the_hour_once(client: TestClient) -> None:
    freeze_shop_clock(MONDAY)
    member = create_member(client)
    create_hoist(client, name="Bay 1")
    shop = create_hoist(client, name="Bay 6", is_shop=True)
    login_member(client, member["email"])
    first = _request(client, shop, _at(7, 10), _at(7, 11))
    second = _request(client, shop, _at(7, 10), _at(7, 11))
    assert first.status_code == 201, first.text
    assert second.status_code == 201, second.text

    approved = client.post(f"/shop-hoist-requests/{first.json()['id']}/approve", headers=AUTH)
    assert approved.status_code == 200, approved.text
    assert approved.json()["booking_id"]

    overlap = client.post(f"/shop-hoist-requests/{second.json()['id']}/approve", headers=AUTH)
    assert overlap.status_code == 409, overlap.text
    assert overlap.json()["error"]["code"] == "hoist_overlap"
    assert client.get("/shop-hoist-requests", headers=AUTH).json()
    still = next(row for row in client.get("/member/shop-hoist-requests").json() if row["id"] == second.json()["id"])
    assert still["status"] == "pending"


def test_closing_the_shop_hoist_cancels_open_requests_and_tells_the_member(client: TestClient) -> None:
    freeze_shop_clock(MONDAY)
    member = create_member(client)
    shop = create_hoist(client, name="Bay 6", is_shop=True)
    login_member(client, member["email"])
    requested = _request(client, shop, _at(7, 12), _at(7, 13))
    assert requested.status_code == 201, requested.text

    closed = client.patch(
        f"/hoists/{shop['id']}",
        headers=AUTH,
        json={"status": "maintenance", "reason": "Lift inspection"},
    )

    assert closed.status_code == 200, closed.text
    stored = client.get("/member/shop-hoist-requests").json()[0]
    assert stored["status"] == "denied"
    notices = [
        row
        for row in client.get("/fill/outbox", headers=AUTH).json()
        if (row.get("payload") or {}).get("kind") == "shop_request_closed"
    ]
    assert len(notices) == 1
    assert notices[0]["member_id"] == member["id"]
    assert "Mountain Time" in notices[0]["body"]
