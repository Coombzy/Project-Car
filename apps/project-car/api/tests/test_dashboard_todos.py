from __future__ import annotations

from datetime import timedelta

from fastapi.testclient import TestClient

from app.shop_time import pricing_now
from tests.conftest import AUTH, create_hoist, create_member, login_member


def _window(hours_from_now: int, length_hours: float = 2) -> tuple[str, str]:
    start = pricing_now() + timedelta(hours=hours_from_now)
    end = start + timedelta(hours=length_hours)
    return start.isoformat(), end.isoformat()


def test_dashboard_next_24h_hours_and_parts_orders(client: TestClient) -> None:
    member = create_member(client)
    hoist = create_hoist(client, name="Bay 1")
    start, end = _window(1)
    created = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": start,
            "end_at": end,
            "notes": "1992 Miata — clutch",
        },
    )
    assert created.status_code == 201, created.text

    denied = client.get("/dashboard")
    assert denied.status_code == 401

    dash = client.get("/dashboard", headers=AUTH)
    assert dash.status_code == 200, dash.text
    body = dash.json()
    assert body["tz"] == "America/Regina"
    assert "window_start" in body
    assert "window_end" in body
    assert body["todos"] == []
    assert body["parts_orders"] == []
    assert body["calendar"]["google"]["connected"] is False
    assert body["calendar"]["apple"]["status"] == "ics_only"

    bay = next(row for row in body["hoists"] if row["name"] == "Bay 1")
    hours = bay["next_hours"]
    assert len(hours) >= 2
    assert {row["vehicle_label"] for row in hours} == {"1992 Miata — clutch"}
    assert hours[0]["member_name"] == "Ada Reyes"
    assert hours[0]["hour_start"] < hours[1]["hour_start"]


def test_booked_hour_uses_notes_placeholder_without_vehicle(client: TestClient) -> None:
    member = create_member(client)
    hoist = create_hoist(client, name="Bay 2")
    start, end = _window(2)
    created = client.post(
        "/bookings",
        headers=AUTH,
        json={"member_id": member["id"], "hoist_id": hoist["id"], "start_at": start, "end_at": end},
    )
    assert created.status_code == 201, created.text
    dash = client.get("/dashboard", headers=AUTH)
    bay = next(row for row in dash.json()["hoists"] if row["name"] == "Bay 2")
    assert bay["next_hours"][0]["vehicle_label"] == "No vehicle on file"


def test_owner_and_member_todos_are_isolated(client: TestClient) -> None:
    ada = create_member(client, email="ada@example.com")
    create_member(client, name="Casey", email="casey@example.com", tier_name="basic")

    owner_created = client.post(
        "/todos",
        headers=AUTH,
        json={"title": "Call Priya", "notes": "Waitlist follow-up"},
    )
    assert owner_created.status_code == 201, owner_created.text
    owner_id = owner_created.json()["id"]

    login_member(client, "ada@example.com")
    ada_created = client.post("/todos", json={"title": "Bring turbo parts"})
    assert ada_created.status_code == 201, ada_created.text
    ada_id = ada_created.json()["id"]

    listed = client.get("/todos")
    assert listed.status_code == 200
    assert [row["title"] for row in listed.json()] == ["Bring turbo parts"]
    assert client.get(f"/todos/{owner_id}").status_code == 404
    stolen = client.patch(f"/todos/{owner_id}", json={"status": "done"})
    assert stolen.status_code == 404

    owner_list = client.get("/todos", headers=AUTH)
    assert [row["title"] for row in owner_list.json()] == ["Call Priya"]
    assert client.delete(f"/todos/{ada_id}", headers=AUTH).status_code == 404

    done = client.patch(f"/todos/{ada_id}", json={"status": "done"})
    assert done.status_code == 200
    assert done.json()["status"] == "done"

    ics = client.get(f"/todos/{ada_id}/ics")
    assert ics.status_code == 200
    assert "BEGIN:VCALENDAR" in ics.text
    assert "TZID=America/Regina" in ics.text
    assert "Bring turbo parts" in ics.text
    assert ics.headers["content-type"].startswith("text/calendar")

    assert client.delete(f"/todos/{ada_id}").status_code == 204
    assert client.get("/todos").json() == []
    assert client.get(f"/todos/{owner_id}", headers=AUTH).status_code == 200

    dash = client.get("/dashboard", headers=AUTH)
    assert any(row["title"] == "Call Priya" for row in dash.json()["todos"])

    member_dash = client.get("/member/dashboard")
    assert member_dash.status_code == 200
    assert member_dash.json()["todos"] == []
    assert member_dash.json()["hoists"] == []
    assert member_dash.json()["tz"] == "America/Regina"
    _ = ada


def test_member_dashboard_only_shows_own_next_hours(client: TestClient) -> None:
    ada = create_member(client, email="ada@example.com")
    casey = create_member(client, name="Casey", email="casey@example.com", tier_name="basic")
    bay = create_hoist(client, name="Bay 1")
    shop = create_hoist(client, name="Bay 6", is_shop=True)
    start, end = _window(3)
    other_start, other_end = _window(5)
    shop_start, shop_end = _window(4)
    assert (
        client.post(
            "/bookings",
            headers=AUTH,
            json={
                "member_id": ada["id"],
                "hoist_id": bay["id"],
                "start_at": start,
                "end_at": end,
                "notes": "Ada’s Miata",
            },
        ).status_code
        == 201
    )
    assert (
        client.post(
            "/bookings",
            headers=AUTH,
            json={
                "member_id": casey["id"],
                "hoist_id": bay["id"],
                "start_at": other_start,
                "end_at": other_end,
                "notes": "Casey only",
            },
        ).status_code
        == 201
    )
    shop_booking = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "hoist_id": shop["id"],
            "start_at": shop_start,
            "end_at": shop_end,
            "kind": "shop",
            "notes": "Owner rack work",
        },
    )
    assert shop_booking.status_code == 201, shop_booking.text

    login_member(client, "ada@example.com")
    body = client.get("/member/dashboard").json()
    assert [row["name"] for row in body["hoists"]] == ["Bay 1"]
    hours = body["hoists"][0]["next_hours"]
    assert hours
    assert all(row["member_name"] == "Ada Reyes" for row in hours)
    assert all(row["vehicle_label"] == "Ada’s Miata" for row in hours)
    assert all(row["hoist_name"] != "Bay 6" for row in hours)


def test_calendar_connect_is_stubbed(client: TestClient) -> None:
    status = client.get("/calendar/status", headers=AUTH)
    assert status.status_code == 200
    assert status.json()["google"]["ready"] is False
    start = client.get("/calendar/google/start", headers=AUTH)
    assert start.status_code == 501
    assert start.json()["error"]["code"] == "calendar_oauth_not_configured"
    apple = client.get("/calendar/apple/start", headers=AUTH)
    assert apple.status_code == 501
    assert apple.json()["error"]["code"] == "apple_calendar_ics_only"


def test_seed_includes_bay6_todos_and_parts_orders(client: TestClient) -> None:
    from app.db import get_db
    from app.main import app
    from app.seed import seed

    override = app.dependency_overrides[get_db]
    session_gen = override()
    session = next(session_gen)
    try:
        summary = seed(session, reset=True)
        session.commit()
    finally:
        session_gen.close()

    assert summary["todos"] >= 6
    assert summary["parts_orders"] >= 3
    dash = client.get("/dashboard", headers=AUTH)
    assert dash.status_code == 200
    body = dash.json()
    names = [row["name"] for row in body["hoists"]]
    assert names == ["Bay 1", "Bay 2", "Bay 3", "Bay 4", "Bay 5", "Bay 6"]
    shop = next(row for row in body["hoists"] if row["is_shop"])
    assert shop["name"] == "Bay 6"
    for name in names:
        bay = next(row for row in body["hoists"] if row["name"] == name)
        assert bay["next_hours"], f"{name} should show booked hours in the next 24h"
    assert any(hour["member_name"] == "Ada Reyes" for hour in body["hoists"][0]["next_hours"])
    assert any(hour["member_name"] == "Shop" for hour in shop["next_hours"])
    assert any("Miata" in hour["vehicle_label"] for hour in body["hoists"][0]["next_hours"])
    assert any(row["title"] for row in body["todos"])
    skus = {row["sku"] for row in body["parts_orders"]}
    assert any(sku and sku.startswith("PT-") for sku in skus)
    assert {row["status"] for row in body["parts_orders"]} <= {
        "ordered",
        "shipped",
        "in_transit",
        "received",
    }

    login_member(client, "ada.reyes@example.com")
    member = client.get("/member/dashboard")
    assert member.status_code == 200
    assert any(row["title"] for row in member.json()["todos"])
