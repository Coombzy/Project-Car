"""Shop hoist requests. Pending is not a booking and does not move tokens."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

from fastapi.testclient import TestClient

from app.config import get_settings
from tests.conftest import AUTH, create_hoist, create_member, login_member, next_hour

REPO = Path(__file__).resolve().parents[4]
AI = {"Authorization": "Bearer dev-ai-secret"}


def _window(hours_from_now: int, length_hours: float = 1) -> tuple[str, str]:
    start = next_hour(hours_from_now)
    end = start + timedelta(hours=length_hours)
    return start.isoformat(), end.isoformat()


def _dec(value) -> Decimal:
    return Decimal(str(value))


def _balance(client: TestClient, member_id: str) -> Decimal:
    response = client.get(f"/members/{member_id}", headers=AUTH)
    assert response.status_code == 200, response.text
    return _dec(response.json()["token_balance"])


def _ledger(client: TestClient, member_id: str) -> list[dict]:
    response = client.get(f"/members/{member_id}/tokens", headers=AUTH)
    assert response.status_code == 200, response.text
    return response.json()


def _booking_ids(client: TestClient) -> list[str]:
    response = client.get("/bookings", headers=AUTH)
    assert response.status_code == 200, response.text
    return [row["id"] for row in response.json()]


def test_member_request_is_pending_and_does_not_debit(client: TestClient) -> None:
    member = create_member(client, email="ada@example.com")
    shop = create_hoist(client, name="Shop", location_label="Internal", is_shop=True)
    start, end = _window(8)
    login_member(client, "ada@example.com")
    balance = _dec(client.get("/member/me").json()["token_balance"])
    ledger_before = client.get("/member/tokens").json()

    created = client.post(
        "/member/shop-hoist-requests",
        json={"hoist_id": shop["id"], "start_at": start, "end_at": end, "notes": "Need the hoist"},
    )
    assert created.status_code == 201, created.text
    body = created.json()
    assert body["record"] == "shop_hoist_request"
    assert body["status"] == "pending"
    assert body["member_id"] == member["id"]
    assert body["hoist_id"] == shop["id"]
    assert _dec(body["token_quote"]) > 0
    assert _dec(client.get("/member/me").json()["token_balance"]) == balance
    assert client.get("/member/tokens").json() == ledger_before
    assert client.get("/member/bookings").json() == []

    listed = client.get("/member/shop-hoist-requests")
    assert listed.status_code == 200
    assert [row["id"] for row in listed.json()] == [body["id"]]
    assert listed.json()[0]["status"] == "pending"

    owner_view = client.get("/bookings", headers=AUTH, params={"hoist_id": shop["id"]})
    assert owner_view.status_code == 200
    assert owner_view.json() == []


def test_two_pending_requests_do_not_hold_the_hour(client: TestClient) -> None:
    ada = create_member(client, name="Ada Reyes", email="ada@example.com")
    sam = create_member(client, name="Sam Okonkwo", email="sam@example.com")
    shop = create_hoist(client, name="Shop", is_shop=True)
    start, end = _window(6)

    login_member(client, "ada@example.com")
    first = client.post(
        "/member/shop-hoist-requests",
        json={"hoist_id": shop["id"], "start_at": start, "end_at": end},
    )
    assert first.status_code == 201, first.text

    client.post("/auth/member/logout")
    login_member(client, "sam@example.com")
    second = client.post(
        "/member/shop-hoist-requests",
        json={"hoist_id": shop["id"], "start_at": start, "end_at": end},
    )
    assert second.status_code == 201, second.text
    assert second.json()["id"] != first.json()["id"]
    assert second.json()["status"] == "pending"

    bookings = client.get("/bookings", headers=AUTH, params={"hoist_id": shop["id"]})
    assert bookings.json() == []
    requests = client.get("/shop-hoist-requests", headers=AUTH)
    assert requests.status_code == 200
    assert {row["member_id"] for row in requests.json()} == {ada["id"], sam["id"]}
    assert all(row["status"] == "pending" for row in requests.json())
    assert _balance(client, ada["id"]) == Decimal("1500")
    assert _balance(client, sam["id"]) == Decimal("1500")


def test_bays_stay_a_direct_booking(client: TestClient) -> None:
    member = create_member(client, email="ada@example.com")
    bay = create_hoist(client, name="Bay 1")
    create_hoist(client, name="Shop", is_shop=True)
    start, end = _window(5)
    login_member(client, "ada@example.com")
    balance = _dec(client.get("/member/me").json()["token_balance"])

    booked = client.post(
        "/member/bookings",
        json={"hoist_id": bay["id"], "start_at": start, "end_at": end},
    )
    assert booked.status_code == 201, booked.text
    body = booked.json()
    assert body["kind"] == "customer"
    assert body["status"] == "pending"
    assert "record" not in body
    assert _dec(client.get("/member/me").json()["token_balance"]) == balance - _dec(body["reserved_tokens"])
    assert client.get("/member/bookings").json()[0]["id"] == body["id"]

    hoists = client.get("/member/hoists")
    assert {row["name"] for row in hoists.json()} == {"Bay 1"}
    shop = client.get("/member/shop-hoist")
    assert shop.status_code == 200
    assert shop.json()["name"] == "Shop"
    assert shop.json()["is_shop"] is True


def test_request_is_not_auto_approved(client: TestClient) -> None:
    create_member(client, email="ada@example.com")
    shop = create_hoist(client, name="Shop", is_shop=True)
    start, end = _window(9)
    login_member(client, "ada@example.com")
    created = client.post(
        "/member/shop-hoist-requests",
        json={"hoist_id": shop["id"], "start_at": start, "end_at": end},
    )
    assert created.status_code == 201, created.text
    request_id = created.json()["id"]
    assert created.json()["status"] == "pending"

    confirm = client.post(f"/member/bookings/{request_id}/confirm")
    assert confirm.status_code == 404
    still = client.get("/member/shop-hoist-requests")
    assert still.json()[0]["status"] == "pending"
    assert client.get("/bookings", headers=AUTH, params={"hoist_id": shop["id"]}).json() == []


def test_owner_customer_post_is_a_request(client: TestClient) -> None:
    member = create_member(client)
    shop = create_hoist(client, name="Shop", is_shop=True)
    start, end = _window(7)
    balance = _balance(client, member["id"])
    created = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": shop["id"],
            "start_at": start,
            "end_at": end,
        },
    )
    assert created.status_code == 201, created.text
    assert created.json()["record"] == "shop_hoist_request"
    assert created.json()["status"] == "pending"
    assert created.json()["created_by_kind"] == "human"
    assert _balance(client, member["id"]) == balance
    assert "shop_hoist_owner_only" not in created.text


def test_ai_created_shop_hoist_request_cannot_be_self_approved(client: TestClient) -> None:
    """POST /bookings stores the real actor, so the same AI cannot approve it.

    A human owner create stays human, and that AI can still approve the human request.
    """
    member = create_member(client, email="ada@example.com")
    shop = create_hoist(client, name="Shop", is_shop=True)
    start, end = _window(11)
    balance = _balance(client, member["id"])
    ledger_before = _ledger(client, member["id"])
    actor_id = get_settings().ai_actor_id

    created = client.post(
        "/bookings",
        headers=AI,
        json={
            "member_id": member["id"],
            "hoist_id": shop["id"],
            "start_at": start,
            "end_at": end,
        },
    )
    assert created.status_code == 201, created.text
    body = created.json()
    assert body["record"] == "shop_hoist_request"
    assert body["status"] == "pending"
    assert body["member_id"] == member["id"]
    assert body["hoist_id"] == shop["id"]

    blocked = client.post(f"/shop-hoist-requests/{body['id']}/approve", headers=AI)
    reserve_kinds = [
        row["kind"] for row in _ledger(client, member["id"]) if row["kind"] == "booking_reserve"
    ]
    assert blocked.status_code == 403, (
        f"status={blocked.status_code} reserves={reserve_kinds} body={blocked.text}"
    )
    assert blocked.json()["error"]["code"] == "cannot_approve_own_request"
    assert reserve_kinds == []
    assert _ledger(client, member["id"]) == ledger_before
    assert _balance(client, member["id"]) == balance
    assert client.get("/bookings", headers=AUTH, params={"hoist_id": shop["id"]}).json() == []

    stored = client.get("/shop-hoist-requests", headers=AUTH).json()
    ai_row = next(row for row in stored if row["id"] == body["id"])
    assert body["created_by_kind"] == "ai"
    assert body["created_by_id"] == actor_id
    assert ai_row["created_by_kind"] == "ai"
    assert ai_row["created_by_id"] == actor_id
    assert ai_row["status"] == "pending"
    assert ai_row["booking_id"] is None

    human_start, human_end = _window(22)
    human = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": shop["id"],
            "start_at": human_start,
            "end_at": human_end,
        },
    )
    assert human.status_code == 201, human.text
    assert human.json()["record"] == "shop_hoist_request"
    assert human.json()["created_by_kind"] == "human"
    assert human.json()["created_by_id"] == get_settings().owner_email

    approved = client.post(f"/shop-hoist-requests/{human.json()['id']}/approve", headers=AI)
    assert approved.status_code == 200, approved.text
    assert approved.json()["status"] == "approved"
    assert approved.json()["actor_kind"] == "ai"
    assert approved.json()["request_id"] == human.json()["id"]
    assert [row["kind"] for row in _ledger(client, member["id"]) if row["kind"] == "booking_reserve"] == [
        "booking_reserve"
    ]
    assert _balance(client, member["id"]) == balance - _dec(human.json()["token_quote"])
    bookings = client.get("/bookings", headers=AUTH, params={"hoist_id": shop["id"]}).json()
    assert [row["id"] for row in bookings] == [approved.json()["booking_id"]]


def test_shop_work_on_the_shop_hoist_stays_a_booking(client: TestClient) -> None:
    shop = create_hoist(client, name="Shop", is_shop=True)
    start, end = _window(4)
    created = client.post(
        "/bookings",
        headers=AUTH,
        json={"kind": "shop", "hoist_id": shop["id"], "start_at": start, "end_at": end},
    )
    assert created.status_code == 201, created.text
    assert created.json()["kind"] == "shop"
    assert _dec(created.json()["reserved_tokens"]) == Decimal("0")


def test_shop_hoist_approval_respects_pending_hold_and_simultaneous_cap(client: TestClient) -> None:
    """Pending bookings hold the shop hour, and the tier cap applies at approval."""
    ada = create_member(client, name="Ada Reyes", email="ada@example.com", tier_name="premium")
    sam = create_member(client, name="Sam Okonkwo", email="sam@example.com", tier_name="basic")
    shop = create_hoist(client, name="Shop", is_shop=True)
    bay = create_hoist(client, name="Bay 1")
    held_start, held_end = _window(8)
    bay_start, bay_end = _window(30)
    free_start, free_end = _window(48)

    shop_work = client.post(
        "/bookings",
        headers=AUTH,
        json={"kind": "shop", "hoist_id": shop["id"], "start_at": held_start, "end_at": held_end},
    )
    assert shop_work.status_code == 201, shop_work.text
    assert shop_work.json()["status"] == "pending"
    assert shop_work.json()["kind"] == "shop"

    login_member(client, "ada@example.com")
    overlapping = client.post(
        "/member/shop-hoist-requests",
        json={"hoist_id": shop["id"], "start_at": held_start, "end_at": held_end},
    )
    assert overlapping.status_code == 201, overlapping.text

    held = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": sam["id"],
            "hoist_id": bay["id"],
            "start_at": bay_start,
            "end_at": bay_end,
        },
    )
    assert held.status_code == 201, held.text
    assert held.json()["status"] == "pending"

    client.post("/auth/member/logout")
    login_member(client, "sam@example.com")
    capped_request = client.post(
        "/member/shop-hoist-requests",
        json={"hoist_id": shop["id"], "start_at": free_start, "end_at": free_end},
    )
    assert capped_request.status_code == 201, capped_request.text

    ada_ledger = _ledger(client, ada["id"])
    ada_balance = _balance(client, ada["id"])
    bookings_before = _booking_ids(client)

    overlap = client.post(f"/shop-hoist-requests/{overlapping.json()['id']}/approve", headers=AUTH)
    cap = client.post(f"/shop-hoist-requests/{capped_request.json()['id']}/approve", headers=AUTH)

    assert overlap.status_code == 409, overlap.text
    assert overlap.json()["error"]["code"] == "hoist_overlap"
    assert _ledger(client, ada["id"]) == ada_ledger
    assert _balance(client, ada["id"]) == ada_balance
    shop_rows = client.get("/bookings", headers=AUTH, params={"hoist_id": shop["id"]}).json()
    assert [row["id"] for row in shop_rows] == [shop_work.json()["id"]]

    assert cap.status_code == 400, cap.text
    assert cap.json()["error"]["code"] == "max_simultaneous_bookings"
    assert _booking_ids(client) == bookings_before
    still = client.get(
        "/shop-hoist-requests",
        headers=AUTH,
        params={"status": "pending"},
    ).json()
    assert {row["id"] for row in still} == {overlapping.json()["id"], capped_request.json()["id"]}
    assert all(row["booking_id"] is None for row in still)


def test_past_shop_hoist_start_is_rejected(client: TestClient) -> None:
    """A shop-hoist request whose start is already past is not stored and does not move tokens."""
    member = create_member(client, email="ada@example.com")
    shop = create_hoist(client, name="Shop", is_shop=True)
    past = datetime(2020, 6, 2, 16, 0, tzinfo=timezone.utc)
    past_end = past + timedelta(hours=1)
    balance = _balance(client, member["id"])
    ledger = _ledger(client, member["id"])

    login_member(client, "ada@example.com")
    member_request = client.post(
        "/member/shop-hoist-requests",
        json={
            "hoist_id": shop["id"],
            "start_at": past.isoformat(),
            "end_at": past_end.isoformat(),
        },
    )
    assert member_request.status_code == 400, member_request.text
    assert member_request.json()["error"]["code"] == "start_in_past"
    assert client.get("/member/shop-hoist-requests").json() == []
    assert client.get("/member/bookings").json() == []

    owner_request = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": shop["id"],
            "start_at": past.isoformat(),
            "end_at": past_end.isoformat(),
        },
    )
    assert owner_request.status_code == 400, owner_request.text
    assert owner_request.json()["error"]["code"] == "start_in_past"
    listed = client.get("/shop-hoist-requests", headers=AUTH)
    assert listed.status_code == 200, listed.text
    assert listed.json() == []
    assert client.get("/bookings", headers=AUTH).json() == []
    assert _balance(client, member["id"]) == balance
    assert _ledger(client, member["id"]) == ledger


def test_approve_after_the_start_has_passed_does_not_book(client: TestClient, monkeypatch) -> None:
    """Approving once shop now is past start_at does not book or charge.

    The window has started and has not ended. The request stays pending, so
    staff can still decline it. A request whose start is still ahead still
    approves. Red on main: that approve returns 200 and writes a booking.
    """
    monkeypatch.setenv("SHOP_NOW", "2026-10-06T15:00:00-06:00")
    member = create_member(client, email="ada.past-window@example.com")
    shop = create_hoist(client, name="Shop", is_shop=True)
    soon_start, soon_end = _window(2)
    later_start, later_end = _window(24 * 10)
    opened = datetime.fromisoformat(soon_start) + timedelta(minutes=30)
    assert datetime.fromisoformat(soon_start) < opened < datetime.fromisoformat(soon_end)

    soon = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": shop["id"],
            "start_at": soon_start,
            "end_at": soon_end,
        },
    )
    assert soon.status_code == 201, soon.text
    assert soon.json()["record"] == "shop_hoist_request"
    assert soon.json()["status"] == "pending"
    later = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": shop["id"],
            "start_at": later_start,
            "end_at": later_end,
        },
    )
    assert later.status_code == 201, later.text
    assert later.json()["status"] == "pending"
    ledger = _ledger(client, member["id"])
    balance = _balance(client, member["id"])
    assert client.get("/bookings", headers=AUTH, params={"hoist_id": shop["id"]}).json() == []

    monkeypatch.setenv("SHOP_NOW", opened.isoformat())
    approved = client.post(f"/shop-hoist-requests/{soon.json()['id']}/approve", headers=AUTH)
    assert approved.status_code == 400, approved.text
    assert approved.json()["error"]["code"] == "start_in_past"

    pending = client.get("/shop-hoist-requests", headers=AUTH, params={"status": "pending"}).json()
    assert {row["id"] for row in pending} == {soon.json()["id"], later.json()["id"]}
    assert all(row["status"] == "pending" and row["booking_id"] is None for row in pending)
    assert client.get("/bookings", headers=AUTH, params={"hoist_id": shop["id"]}).json() == []
    assert _ledger(client, member["id"]) == ledger
    assert _balance(client, member["id"]) == balance

    denied = client.post(f"/shop-hoist-requests/{soon.json()['id']}/deny", headers=AUTH)
    assert denied.status_code == 200, denied.text
    assert denied.json()["status"] == "denied"
    assert denied.json()["booking_id"] is None
    assert denied.json()["request_id"] == soon.json()["id"]
    listed = client.get("/shop-hoist-requests", headers=AUTH).json()
    soon_row = next(row for row in listed if row["id"] == soon.json()["id"])
    assert soon_row["status"] == "denied"
    assert soon_row["booking_id"] is None
    assert client.get("/bookings", headers=AUTH, params={"hoist_id": shop["id"]}).json() == []
    assert _ledger(client, member["id"]) == ledger
    assert _balance(client, member["id"]) == balance

    still_open = client.post(f"/shop-hoist-requests/{later.json()['id']}/approve", headers=AUTH)
    assert still_open.status_code == 200, still_open.text
    assert still_open.json()["status"] == "approved"
    assert still_open.json()["booking_id"]
    bookings = client.get("/bookings", headers=AUTH, params={"hoist_id": shop["id"]}).json()
    assert [row["id"] for row in bookings] == [still_open.json()["booking_id"]]
    assert bookings[0]["status"] == "confirmed"
    reserves = [row for row in _ledger(client, member["id"]) if row["kind"] == "booking_reserve"]
    assert len(reserves) == 1
    assert _balance(client, member["id"]) == balance - _dec(later.json()["token_quote"])


def _record_scalars(monkeypatch, reads: list[tuple[str, bool]]) -> None:
    """Compile each ORM read on the postgresql dialect.

    SQLite drops FOR UPDATE at execution. The statement still carries the
    lock, which is what Postgres will take.
    """
    from sqlalchemy.dialects import postgresql
    from sqlalchemy.orm import Session

    original = Session.scalars

    def spy(self, statement, *args, **kwargs):
        sql = str(statement.compile(dialect=postgresql.dialect()))
        locked = getattr(statement, "_for_update_arg", None) is not None
        reads.append((sql, locked))
        return original(self, statement, *args, **kwargs)

    monkeypatch.setattr(Session, "scalars", spy)


def test_overlapping_shop_hoist_approval_locks_the_request(client: TestClient, monkeypatch) -> None:
    """Approve selects the request FOR UPDATE before the pending check.

    Two overlapping approvals otherwise both read pending, then both insert a
    confirmed booking and a booking_reserve. The loser is 400 invalid_transition
    and leaves the one booking and the one reserve. SQLite drops FOR UPDATE;
    this checks the statement still asks for the lock, before the member lock
    and before any booking read. Red on main: that request select has no FOR UPDATE.
    """
    member = create_member(client, email="ada.overlap@example.com")
    shop = create_hoist(client, name="Shop", is_shop=True)
    start, end = _window(12)
    requested = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": shop["id"],
            "start_at": start,
            "end_at": end,
        },
    )
    assert requested.status_code == 201, requested.text
    assert requested.json()["record"] == "shop_hoist_request"
    assert requested.json()["status"] == "pending"
    request_id = requested.json()["id"]

    reads: list[tuple[str, bool]] = []
    _record_scalars(monkeypatch, reads)
    approved = client.post(f"/shop-hoist-requests/{request_id}/approve", headers=AUTH)
    assert approved.status_code == 200, approved.text
    assert approved.json()["status"] == "approved"
    assert approved.json()["booking_id"]
    approve_reads = list(reads)

    bookings = client.get("/bookings", headers=AUTH, params={"hoist_id": shop["id"]}).json()
    assert len(bookings) == 1
    assert bookings[0]["id"] == approved.json()["booking_id"]
    assert bookings[0]["status"] == "confirmed"
    ledger = _ledger(client, member["id"])
    reserves = [row for row in ledger if row["kind"] == "booking_reserve"]
    assert len(reserves) == 1
    balance = _balance(client, member["id"])

    reads.clear()
    second = client.post(f"/shop-hoist-requests/{request_id}/approve", headers=AUTH)
    second_reads = list(reads)
    assert second.status_code == 400, second.text
    assert second.json()["error"]["code"] == "invalid_transition"
    assert client.get("/bookings", headers=AUTH, params={"hoist_id": shop["id"]}).json() == bookings
    assert _ledger(client, member["id"]) == ledger
    assert _balance(client, member["id"]) == balance

    request_selects = [
        (index, sql, locked)
        for index, (sql, locked) in enumerate(approve_reads)
        if "FROM shop_hoist_requests" in sql and "shop_hoist_requests.id" in sql
    ]
    assert request_selects, "approve did not select the shop hoist request"
    first_index, first_sql, first_locked = request_selects[0]
    assert first_locked and "FOR UPDATE" in first_sql, (
        "approve request select has no FOR UPDATE on the postgresql dialect"
    )
    member_locks = [
        index
        for index, (sql, locked) in enumerate(approve_reads)
        if locked and "FOR UPDATE" in sql and "FROM members" in sql and "WHERE members.id" in sql
    ]
    assert member_locks, "shop-hoist approve member select has no FOR UPDATE on the postgresql dialect"
    assert first_index < member_locks[0]
    booking_reads = [index for index, (sql, _) in enumerate(approve_reads) if "FROM bookings" in sql]
    assert booking_reads and first_index < booking_reads[0]
    loser_selects = [
        (sql, locked)
        for sql, locked in second_reads
        if "FROM shop_hoist_requests" in sql and "shop_hoist_requests.id" in sql
    ]
    assert loser_selects, "second approve did not select the shop hoist request"
    loser_sql, loser_locked = loser_selects[0]
    assert loser_locked and "FOR UPDATE" in loser_sql, (
        "approve request select has no FOR UPDATE on the postgresql dialect"
    )
    assert not any("FROM bookings" in sql for sql, _locked in second_reads)


def test_deny_shop_hoist_request_locks_the_request(client: TestClient, monkeypatch) -> None:
    """Deny selects the request FOR UPDATE before the pending check.

    A deny that starts while an approve holds the row otherwise reads pending,
    waits on the later UPDATE, and stores denied over a confirmed booking and
    a booking_reserve. The loser is 400 invalid_transition. SQLite drops
    FOR UPDATE; this checks the statement still asks for the lock. The reload
    after the decision is not the gate. Red on main: that request select has
    no FOR UPDATE.
    """
    member = create_member(client, email="ada.deny-lock@example.com")
    shop = create_hoist(client, name="Shop", is_shop=True)
    start, end = _window(13)
    requested = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": shop["id"],
            "start_at": start,
            "end_at": end,
        },
    )
    assert requested.status_code == 201, requested.text
    assert requested.json()["record"] == "shop_hoist_request"
    assert requested.json()["status"] == "pending"
    request_id = requested.json()["id"]
    balance = _balance(client, member["id"])
    ledger = _ledger(client, member["id"])

    reads: list[tuple[str, bool]] = []
    _record_scalars(monkeypatch, reads)
    denied = client.post(f"/shop-hoist-requests/{request_id}/deny", headers=AUTH)
    deny_reads = list(reads)
    assert denied.status_code == 200, denied.text
    body = denied.json()
    assert body["request_id"] == request_id
    assert body["status"] == "denied"
    assert body["action"] == "deny"
    assert body["actor_kind"] == "human"
    assert body["booking_id"] is None
    assert body["action_id"]
    assert client.get("/bookings", headers=AUTH, params={"hoist_id": shop["id"]}).json() == []
    assert _ledger(client, member["id"]) == ledger
    assert _balance(client, member["id"]) == balance

    request_selects = [
        (sql, locked)
        for sql, locked in deny_reads
        if "FROM shop_hoist_requests" in sql and "shop_hoist_requests.id" in sql
    ]
    assert request_selects, "deny did not select the shop hoist request"
    first_sql, first_locked = request_selects[0]
    assert first_locked and "FOR UPDATE" in first_sql, (
        "deny request select has no FOR UPDATE on the postgresql dialect"
    )


def test_deny_after_approve_keeps_the_booking_and_reserve(client: TestClient) -> None:
    """A deny after a finished approve is 400 invalid_transition.

    The confirmed booking and the booking_reserve stay, and the request stays
    approved.
    """
    member = create_member(client, email="ada.deny-after@example.com")
    shop = create_hoist(client, name="Shop", is_shop=True)
    start, end = _window(15)
    requested = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": shop["id"],
            "start_at": start,
            "end_at": end,
        },
    )
    assert requested.status_code == 201, requested.text
    request_id = requested.json()["id"]

    approved = client.post(f"/shop-hoist-requests/{request_id}/approve", headers=AUTH)
    assert approved.status_code == 200, approved.text
    assert approved.json()["status"] == "approved"
    booking_id = approved.json()["booking_id"]
    assert booking_id
    bookings = client.get("/bookings", headers=AUTH, params={"hoist_id": shop["id"]}).json()
    assert [row["id"] for row in bookings] == [booking_id]
    assert bookings[0]["status"] == "confirmed"
    ledger = _ledger(client, member["id"])
    reserves = [row for row in ledger if row["kind"] == "booking_reserve"]
    assert len(reserves) == 1
    assert reserves[0]["booking_id"] == booking_id
    balance = _balance(client, member["id"])

    denied = client.post(f"/shop-hoist-requests/{request_id}/deny", headers=AUTH)
    assert denied.status_code == 400, denied.text
    assert denied.json()["error"]["code"] == "invalid_transition"
    assert denied.json()["error"]["message"] == (
        "Only a pending shop hoist request can be denied."
    )
    assert client.get("/bookings", headers=AUTH, params={"hoist_id": shop["id"]}).json() == bookings
    assert _ledger(client, member["id"]) == ledger
    assert _balance(client, member["id"]) == balance
    listed = client.get("/shop-hoist-requests", headers=AUTH).json()
    stored = next(row for row in listed if row["id"] == request_id)
    assert stored["status"] == "approved"
    assert stored["booking_id"] == booking_id


def test_public_pages_do_not_say_the_shop_is_open() -> None:
    roots = [REPO / "apps" / "website" / "html", REPO / "apps" / "project-car" / "web"]
    hits: list[str] = []
    for root in roots:
        for path in root.rglob("*"):
            if path.suffix not in {".html", ".tsx", ".md"}:
                continue
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                lowered = line.lower()
                if "shop is open" not in lowered:
                    continue
                if any(token in lowered for token in ("not", "never", "don't", "do not", "isn't")):
                    continue
                hits.append(f"{path.relative_to(REPO)}:{number}")
    assert hits == []
