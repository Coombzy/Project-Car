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
    assert "next_hours" in body["hoists"][0]
    assert "todos" in body
    assert "parts_orders" in body
    assert body["tz"] == "America/Regina"


def test_tiers_patch(client: TestClient) -> None:
    listed = client.get("/tiers", headers=AUTH)
    assert listed.status_code == 200
    names = {row["name"] for row in listed.json()}
    assert names == {"basic", "premium"}

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
    assert body["tier_name"] == "premium"
    assert body["phone"] == "403-555-0100"
    assert float(body["token_balance"]) == 1500
    assert body["bookings"] == []

    adjusted = client.post(
        f"/members/{member['id']}/tokens",
        headers=AUTH,
        json={"amount": "-1.5", "note": "Owner correction", "reason": "Owner correction"},
    )
    assert adjusted.status_code == 201
    assert adjusted.json()["kind"] == "admin_adjustment"
    refreshed = client.get(f"/members/{member['id']}", headers=AUTH)
    assert float(refreshed.json()["token_balance"]) == 1498.5


def test_rebuild_token_balance_route_matches_ledger(client: TestClient) -> None:
    """A drifted cache is replaced by the ledger sum, and rebuild inserts no row."""
    from decimal import Decimal
    from uuid import UUID

    from app.models import Member

    member = create_member(client)
    member_id = member["id"]
    adjusted = client.post(
        f"/members/{member_id}/tokens",
        headers=AUTH,
        json={"amount": "-1.5", "note": "Owner correction", "reason": "Owner correction"},
    )
    assert adjusted.status_code == 201, adjusted.text

    ledger_before = client.get(f"/members/{member_id}/tokens", headers=AUTH)
    assert ledger_before.status_code == 200, ledger_before.text
    rows_before = ledger_before.json()
    ledger_sum = sum((Decimal(str(row["amount"])) for row in rows_before), Decimal("0"))
    assert ledger_sum == Decimal("1498.5")
    ledger_ids = [row["id"] for row in rows_before]

    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        row = session.get(Member, UUID(member_id))
        assert row is not None
        row.token_balance = Decimal("1.00")
        session.commit()
    finally:
        session.close()

    drifted = client.get(f"/members/{member_id}", headers=AUTH)
    assert drifted.status_code == 200, drifted.text
    assert Decimal(str(drifted.json()["token_balance"])) == Decimal("1.00")

    rebuilt = client.post(f"/members/{member_id}/tokens/rebuild", headers=AUTH)
    cache_after = client.get(f"/members/{member_id}", headers=AUTH).json()["token_balance"]
    assert rebuilt.status_code == 200, (
        f"{rebuilt.status_code} {rebuilt.text}; hand-edited cache stays {cache_after}"
    )
    assert Decimal(str(rebuilt.json()["token_balance"])) == ledger_sum
    assert Decimal(str(cache_after)) == ledger_sum

    ledger_after = client.get(f"/members/{member_id}/tokens", headers=AUTH)
    assert ledger_after.status_code == 200, ledger_after.text
    assert [row["id"] for row in ledger_after.json()] == ledger_ids

    again = client.post(f"/members/{member_id}/tokens/rebuild", headers=AUTH)
    assert again.status_code == 200, again.text
    assert Decimal(str(again.json()["token_balance"])) == ledger_sum
    stayed = client.get(f"/members/{member_id}", headers=AUTH)
    assert Decimal(str(stayed.json()["token_balance"])) == ledger_sum
    ledger_final = client.get(f"/members/{member_id}/tokens", headers=AUTH)
    assert [row["id"] for row in ledger_final.json()] == ledger_ids


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
    assert summary["hoists"] == 6
    assert summary["bookings"] >= 6

    dash = client.get("/dashboard", headers=AUTH)
    assert dash.status_code == 200
    body = dash.json()
    assert body["waitlist_count"] == 4
    assert len(body["hoists"]) == 6
    assert sum(1 for hoist in body["hoists"] if hoist["is_shop"]) == 1
    assert len(body["token_at_risk"]) >= 1
    members = client.get("/members", headers=AUTH)
    assert len(members.json()) == 6
    assert {row["tier_name"] for row in members.json()} <= {"basic", "premium"}
    tiers = {row["name"]: row["included_tokens"] for row in client.get("/tiers", headers=AUTH).json()}
    assert tiers["basic"] == 1000
    assert tiers["premium"] == 1500
    bookings = client.get("/bookings", headers=AUTH)
    body_bookings = bookings.json()
    assert len(body_bookings) >= 6
    assert any(row["kind"] == "shop" for row in body_bookings)


def test_seeded_waitlist_joined_at_follows_the_frozen_shop_clock(client: TestClient, monkeypatch) -> None:
    """Visual shots read Joined from created_at. A wall clock makes the PNG drift."""
    from sqlalchemy import select

    from app.models import WaitlistEntry
    from app.schemas import WaitlistEntryOut
    from app.seed import seed
    from app.shop_time import as_utc, shop_now

    monkeypatch.setenv("SHOP_NOW", "2026-10-06T15:00:00-06:00")
    session_gen = app_session(client)
    session = next(session_gen)
    try:
        seed(session, reset=True)
        session.commit()
        rows = list(session.scalars(select(WaitlistEntry)).all())
    finally:
        session_gen.close()

    assert len(rows) == 4
    expected = as_utc(shop_now())
    assert expected.isoformat() == "2026-10-06T21:00:00+00:00"
    for row in rows:
        assert as_utc(row.created_at) == expected
        # SQLite keeps the shop wall time and drops the offset. The Owner page
        # formats that string, so the visual check needs this exact value.
        assert WaitlistEntryOut.model_validate(row).model_dump(mode="json")["created_at"] == "2026-10-06T15:00:00"


def app_session(client: TestClient):
    from app.db import get_db
    from app.main import app

    override = app.dependency_overrides[get_db]
    return override()
