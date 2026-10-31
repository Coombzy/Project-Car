"""A booked hour must come back as that hour in Mountain Time.

SQLite stores the instant as naive UTC. A timestamp with no offset is read as
shop wall time, which shows 10:00 as 4:00 p.m. The response keeps the offset
so the shop hour survives.
"""

from datetime import datetime

from fastapi.testclient import TestClient

from app.shop_time import PRICING_TZ
from tests.conftest import AUTH, create_hoist, create_member, freeze_shop_clock, login_member


def test_booking_json_keeps_the_mountain_hour(client: TestClient) -> None:
    freeze_shop_clock(datetime(2026, 11, 2, 8, tzinfo=PRICING_TZ))
    member = create_member(client, email="clock@example.com", tier_name="basic")
    hoist = create_hoist(client, name="Bay 1")
    login_member(client, member["email"])
    start = datetime(2026, 11, 2, 10, tzinfo=PRICING_TZ)
    end = datetime(2026, 11, 2, 11, tzinfo=PRICING_TZ)
    created = client.post(
        "/member/bookings",
        json={"hoist_id": hoist["id"], "start_at": start.isoformat(), "end_at": end.isoformat()},
    )
    assert created.status_code == 201, created.text
    stored = datetime.fromisoformat(created.json()["start_at"])
    assert stored.tzinfo is not None
    assert stored.astimezone(PRICING_TZ).hour == 10

    schedule = client.get("/member/schedule")
    assert schedule.status_code == 200, schedule.text
    slot = next(row for row in schedule.json()["occupancy"] if row["booking_id"] == created.json()["id"])
    occupied = datetime.fromisoformat(slot["start_at"])
    assert occupied.tzinfo is not None
    assert occupied.astimezone(PRICING_TZ).hour == 10

    listed = client.get("/bookings", headers=AUTH)
    assert listed.status_code == 200, listed.text
    owner_row = next(row for row in listed.json() if row["id"] == created.json()["id"])
    owner_start = datetime.fromisoformat(owner_row["start_at"])
    assert owner_start.tzinfo is not None
    assert owner_start.astimezone(PRICING_TZ).hour == 10
