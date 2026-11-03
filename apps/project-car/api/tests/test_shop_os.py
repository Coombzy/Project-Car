from __future__ import annotations

from datetime import datetime
from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy import select

from app.models import Booking, BookingHour
from app.seed import seed, seed_id
from app.services.bookings import _hour_key, _stored_utc
from app.shop_time import SHOP_TZ, iter_regina_hours, shop_now
from tests.conftest import AUTH, create_hoist, create_member, freeze_shop_clock

# Same frozen instant as visual/shop-now.txt.
SEEDED_SHOP_NOW = datetime.fromisoformat("2026-10-06T15:00:00-06:00")


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
        json={"amount": "-1.5", "note": "Owner correction"},
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
        json={"amount": "-1.5", "note": "Owner correction"},
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


def test_seeded_get_bookings_sweeps_without_holding_hours_conflict(client: TestClient) -> None:
    """Seeded GET /bookings runs the no-show sweep and must not 500.

    At the visual clock, Bay 6's rack inspection
    (ee86a633-c661-5d7a-8a94-30c39420ab36 on hoist
    4628c30e-68e6-57bf-a2f7-ae35abd1e73a) used to raise HoldingHoursConflict.
    SQLite had stored the shop wall clock with the offset stripped, and the
    sweep read that naive value as UTC, so 18:00 Regina collided with the
    in-house fab hour that really is 18:00 UTC. The afternoon turbo visit,
    which is still in the future, must stay confirmed.
    """
    freeze_shop_clock(SEEDED_SHOP_NOW)
    rack_id = seed_id("booking", "next24-shop")
    fab_id = seed_id("booking", "today-shop")
    afternoon_id = seed_id("booking", "today-confirmed")
    hoist_id = seed_id("hoist", "shop")
    assert rack_id == UUID("ee86a633-c661-5d7a-8a94-30c39420ab36")
    assert hoist_id == UUID("4628c30e-68e6-57bf-a2f7-ae35abd1e73a")

    session_gen = app_session(client)
    session = next(session_gen)
    try:
        seed(session, reset=True)
        session.commit()
    finally:
        session_gen.close()

    listed = client.get("/bookings", headers=AUTH)
    assert listed.status_code == 200, listed.text

    session_gen = app_session(client)
    session = next(session_gen)
    try:
        session.expire_all()
        afternoon = session.get(Booking, afternoon_id)
        rack = session.get(Booking, rack_id)
        assert afternoon is not None and rack is not None
        # 14:00–16:00 Regina is still open at 15:00. A UTC misread of the
        # stored wall clock treats 16:00 as 16:00 UTC, which is already past.
        assert _stored_utc(afternoon.end_at) > _stored_utc(shop_now())
        wanted = iter_regina_hours(_stored_utc(rack.start_at), _stored_utc(rack.end_at))
        owned = {
            _hour_key(row.hour_start): row.booking_id
            for row in session.scalars(select(BookingHour).where(BookingHour.hoist_id == hoist_id)).all()
        }
        for hour_start, _hour_end in wanted:
            assert owned.get(_hour_key(hour_start)) == rack_id
            assert owned.get(_hour_key(hour_start)) != fab_id
    finally:
        session_gen.close()

    by_id = {row["id"]: row for row in listed.json()}
    assert by_id[str(rack_id)]["status"] == "confirmed"
    assert by_id[str(afternoon_id)]["status"] == "confirmed"
    # Wire times are UTC with an offset. 18:00 and 14:00 are the shop hours.
    rack_start = datetime.fromisoformat(by_id[str(rack_id)]["start_at"])
    afternoon_start = datetime.fromisoformat(by_id[str(afternoon_id)]["start_at"])
    assert rack_start.tzinfo is not None and afternoon_start.tzinfo is not None
    assert rack_start.astimezone(SHOP_TZ).hour == 18
    assert afternoon_start.astimezone(SHOP_TZ).hour == 14


def app_session(client: TestClient):
    from app.db import get_db
    from app.main import app

    override = app.dependency_overrides[get_db]
    return override()
