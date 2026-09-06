from __future__ import annotations

from fastapi.testclient import TestClient

from tests.conftest import AUTH, create_hoist, create_member


def test_dashboard_snapshot(client: TestClient) -> None:
    create_member(client)
    create_hoist(client)
    client.post("/waitlist", json={"name": "Priya", "email": "priya@example.com"})

    denied = client.get("/dashboard")
    assert denied.status_code == 401

    dash = client.get("/dashboard", headers=AUTH)
    assert dash.status_code == 200, dash.text
    body = dash.json()
    assert body["waitlist_count"] == 1
    assert len(body["hoists"]) == 1
    assert body["hoists"][0]["name"] == "Bay 1"
    assert "today_bookings" in body
    assert "token_at_risk" in body


def test_tiers_patch(client: TestClient) -> None:
    listed = client.get("/tiers", headers=AUTH)
    assert listed.status_code == 200
    names = {row["name"] for row in listed.json()}
    assert names == {"basic", "pro", "weekly"}

    patched = client.patch(
        "/tiers/basic",
        headers=AUTH,
        json={"included_tokens": 5, "booking_window_days": 10},
    )
    assert patched.status_code == 200
    assert patched.json()["included_tokens"] == 5
    assert patched.json()["booking_window_days"] == 10


def test_member_detail_and_admin_tokens(client: TestClient) -> None:
    member = create_member(client, phone="403-555-0100")
    detail = client.get(f"/members/{member['id']}", headers=AUTH)
    assert detail.status_code == 200
    body = detail.json()
    assert body["tier_name"] == "pro"
    assert body["phone"] == "403-555-0100"
    assert float(body["token_balance"]) == 8
    assert body["bookings"] == []

    adjusted = client.post(
        f"/members/{member['id']}/tokens",
        headers=AUTH,
        json={"amount": "-1.5", "note": "Owner correction"},
    )
    assert adjusted.status_code == 201
    assert adjusted.json()["kind"] == "admin_adjustment"
    refreshed = client.get(f"/members/{member['id']}", headers=AUTH)
    assert float(refreshed.json()["token_balance"]) == 6.5


def test_hoist_status_patch(client: TestClient) -> None:
    hoist = create_hoist(client, name="Bay 3")
    patched = client.patch(
        f"/hoists/{hoist['id']}",
        headers=AUTH,
        json={"status": "maintenance", "location_label": "East wall"},
    )
    assert patched.status_code == 200
    assert patched.json()["status"] == "maintenance"
    assert patched.json()["location_label"] == "East wall"


def test_waitlist_mark_contacted(client: TestClient) -> None:
    created = client.post("/waitlist", json={"name": "Harper", "email": "harper@example.com"})
    assert created.status_code == 201
    assert created.json()["contacted_at"] is None
    marked = client.post(f"/waitlist/{created.json()['id']}/contacted", headers=AUTH)
    assert marked.status_code == 200
    assert marked.json()["contacted_at"] is not None


def test_seed_demo_data_on_sqlite(client: TestClient) -> None:
    from app.db import get_db
    from app.seed import seed

    # Use the same override session pattern by calling seed against a fresh session
    # from the test client app's dependency — easier to seed via the TestingSession
    # created in conftest. Pull one session through the override.
    session_gen = app_session(client)
    session = next(session_gen)
    try:
        summary = seed(session, reset=True)
        session.commit()
    finally:
        session_gen.close()

    assert summary["members"] == 6
    assert summary["hoists"] == 3
    assert summary["bookings"] == 7

    dash = client.get("/dashboard", headers=AUTH)
    assert dash.status_code == 200
    body = dash.json()
    assert body["waitlist_count"] == 4
    assert len(body["hoists"]) == 3
    assert len(body["token_at_risk"]) >= 1
    members = client.get("/members", headers=AUTH)
    assert len(members.json()) == 6
    bookings = client.get("/bookings", headers=AUTH)
    assert len(bookings.json()) == 7


def app_session(client: TestClient):
    from app.db import get_db
    from app.main import app

    override = app.dependency_overrides[get_db]
    return override()
