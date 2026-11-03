"""Approve and deny routes. A human and an AI use the same API."""

from __future__ import annotations

from datetime import timedelta
from decimal import Decimal
from uuid import UUID, uuid4

from fastapi.testclient import TestClient
from sqlalchemy import select

from app.models import Booking, RefundRequest, ShopJob, ShopJobStatus, StaffAction
from app.shop_time import as_utc, shop_now
from tests.conftest import AUTH, create_hoist, create_member, login_member

AI = {"Authorization": "Bearer dev-ai-secret"}


def _window(hours_from_now: int, length_hours: float = 1) -> tuple[str, str]:
    start = shop_now() + timedelta(hours=hours_from_now)
    end = start + timedelta(hours=length_hours)
    return start.isoformat(), end.isoformat()


def _dec(value) -> Decimal:
    return Decimal(str(value))


def _balance(client: TestClient, member_id: str) -> Decimal:
    response = client.get(f"/members/{member_id}", headers=AUTH)
    assert response.status_code == 200, response.text
    return _dec(response.json()["token_balance"])


def _owner_booking(
    client: TestClient,
    member_id: str,
    hoist_id: str,
    hours_from_now: int = 0,
    *,
    minutes_from_now: int = 0,
) -> dict:
    start_dt = shop_now() + timedelta(hours=hours_from_now, minutes=minutes_from_now)
    end_dt = start_dt + timedelta(hours=1)
    start, end = start_dt.isoformat(), end_dt.isoformat()
    created = client.post(
        "/bookings",
        headers=AUTH,
        json={"member_id": member_id, "hoist_id": hoist_id, "start_at": start, "end_at": end},
    )
    assert created.status_code == 201, created.text
    body = created.json()
    assert body["status"] == "pending"
    assert _dec(body["reserved_tokens"]) > 0
    return body


def _stored_booking(client: TestClient, booking_id: str) -> dict:
    rows = client.get("/bookings", headers=AUTH).json()
    match = [row for row in rows if row["id"] == booking_id]
    assert len(match) == 1
    return match[0]


def _booking_ledger(client: TestClient, member_id: str, booking_id: str) -> list[dict]:
    response = client.get(f"/members/{member_id}/tokens", headers=AUTH)
    assert response.status_code == 200, response.text
    return [row for row in response.json() if row["booking_id"] == booking_id]


def _refund_ids(client: TestClient, booking_id: str) -> list[tuple[str, str]]:
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        rows = session.scalars(
            select(RefundRequest)
            .where(RefundRequest.booking_id == UUID(booking_id))
            .order_by(RefundRequest.created_at, RefundRequest.id)
        ).all()
        return [(str(row.id), row.status.value) for row in rows]
    finally:
        session.close()


def _move_into_the_past(client: TestClient, booking_id: str) -> None:
    """Store a UTC end already behind shop now so overdue can flip an active visit."""
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        row = session.get(Booking, UUID(booking_id))
        assert row is not None
        end = as_utc(shop_now() - timedelta(minutes=1))
        row.start_at = end - timedelta(hours=1)
        row.end_at = end
        session.commit()
    finally:
        session.close()


def _refund_request(client: TestClient, request_id: str) -> dict:
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        row = session.get(RefundRequest, UUID(request_id))
        assert row is not None
        decided = row.decided_by_kind.value if row.decided_by_kind is not None else None
        return {
            "status": row.status.value,
            "decided_by_kind": decided,
            "decided_at": row.decided_at,
        }
    finally:
        session.close()


def _request_hoist(client: TestClient, email: str, hoist_id: str, start: str, end: str) -> dict:
    login_member(client, email)
    created = client.post(
        "/member/shop-hoist-requests",
        json={"hoist_id": hoist_id, "start_at": start, "end_at": end},
    )
    assert created.status_code == 201, created.text
    assert created.json()["status"] == "pending"
    return created.json()


def test_approval_reserves_tokens_and_stores_the_human(client: TestClient) -> None:
    member = create_member(client, email="ada@example.com")
    shop = create_hoist(client, name="Shop", is_shop=True)
    start, end = _window(8)
    before = _balance(client, member["id"])
    request = _request_hoist(client, "ada@example.com", shop["id"], start, end)
    assert _balance(client, member["id"]) == before
    assert client.get("/bookings", headers=AUTH, params={"hoist_id": shop["id"]}).json() == []

    approved = client.post(f"/shop-hoist-requests/{request['id']}/approve", headers=AUTH)
    assert approved.status_code == 200, approved.text
    body = approved.json()
    assert body["request_id"] == request["id"]
    assert body["status"] == "approved"
    assert body["actor_kind"] == "human"
    assert body["action"] == "approve"
    assert body["booking_id"]
    assert _dec(body["token_balance"]) == before - _dec(request["token_quote"])
    assert _balance(client, member["id"]) == before - _dec(request["token_quote"])

    bookings = client.get("/bookings", headers=AUTH, params={"hoist_id": shop["id"]}).json()
    assert len(bookings) == 1
    assert bookings[0]["status"] == "confirmed"
    assert bookings[0]["id"] == body["booking_id"]
    listed = client.get("/shop-hoist-requests", headers=AUTH).json()
    assert listed[0]["decided_by_kind"] == "human"
    assert listed[0]["id"] == request["id"]


def test_denial_does_not_debit(client: TestClient) -> None:
    member = create_member(client, email="ada@example.com")
    shop = create_hoist(client, name="Shop", is_shop=True)
    start, end = _window(9)
    before = _balance(client, member["id"])
    request = _request_hoist(client, "ada@example.com", shop["id"], start, end)

    denied = client.post(f"/shop-hoist-requests/{request['id']}/deny", headers=AI)
    assert denied.status_code == 200, denied.text
    assert denied.json()["status"] == "denied"
    assert denied.json()["actor_kind"] == "ai"
    assert denied.json()["request_id"] == request["id"]
    assert denied.json()["booking_id"] is None
    assert _balance(client, member["id"]) == before
    assert client.get("/bookings", headers=AUTH, params={"hoist_id": shop["id"]}).json() == []


def test_second_approval_of_the_same_hour_does_not_debit(client: TestClient) -> None:
    ada = create_member(client, name="Ada Reyes", email="ada@example.com")
    sam = create_member(client, name="Sam Okonkwo", email="sam@example.com")
    shop = create_hoist(client, name="Shop", is_shop=True)
    start, end = _window(6)
    first = _request_hoist(client, "ada@example.com", shop["id"], start, end)
    client.post("/auth/member/logout")
    second = _request_hoist(client, "sam@example.com", shop["id"], start, end)
    ada_before = _balance(client, ada["id"])
    sam_before = _balance(client, sam["id"])

    approved = client.post(f"/shop-hoist-requests/{first['id']}/approve", headers=AUTH)
    assert approved.status_code == 200, approved.text
    ada_after = _balance(client, ada["id"])
    assert ada_after == ada_before - _dec(first["token_quote"])

    blocked = client.post(f"/shop-hoist-requests/{second['id']}/approve", headers=AI)
    assert blocked.status_code == 409
    assert blocked.json()["error"]["code"] == "hoist_overlap"
    assert _balance(client, sam["id"]) == sam_before
    assert _balance(client, ada["id"]) == ada_after
    still = client.get("/shop-hoist-requests", headers=AUTH, params={"status": "pending"}).json()
    assert [row["id"] for row in still] == [second["id"]]
    assert len(client.get("/bookings", headers=AUTH, params={"hoist_id": shop["id"]}).json()) == 1


def test_ai_cannot_approve_its_own_hoist_request(client: TestClient) -> None:
    member = create_member(client, email="ada@example.com")
    shop = create_hoist(client, name="Shop", is_shop=True)
    start, end = _window(10)
    before = _balance(client, member["id"])
    created = client.post(
        "/shop-hoist-requests",
        headers=AI,
        json={"member_id": member["id"], "hoist_id": shop["id"], "start_at": start, "end_at": end},
    )
    assert created.status_code == 201, created.text
    assert created.json()["created_by_kind"] == "ai"
    assert created.json()["status"] == "pending"

    blocked = client.post(f"/shop-hoist-requests/{created.json()['id']}/approve", headers=AI)
    assert blocked.status_code == 403
    assert blocked.json()["error"]["code"] == "cannot_approve_own_request"
    assert _balance(client, member["id"]) == before
    assert client.get("/bookings", headers=AUTH, params={"hoist_id": shop["id"]}).json() == []

    approved = client.post(f"/shop-hoist-requests/{created.json()['id']}/approve", headers=AUTH)
    assert approved.status_code == 200, approved.text
    assert approved.json()["actor_kind"] == "human"
    assert approved.json()["request_id"] == created.json()["id"]
    assert _balance(client, member["id"]) == before - _dec(created.json()["token_quote"])


def test_parts_and_tool_crib_use_the_same_decision_routes(client: TestClient) -> None:
    member = create_member(client, email="ada@example.com")
    before = _balance(client, member["id"])
    parts = client.post(
        "/parts-requests",
        headers=AI,
        json={"member_id": member["id"], "sku": "PT-OIL-5W30-012", "note": "Need oil"},
    )
    assert parts.status_code == 201, parts.text
    own = client.post(f"/parts-requests/{parts.json()['id']}/approve", headers=AI)
    assert own.status_code == 403
    assert own.json()["error"]["code"] == "cannot_approve_own_request"
    approved = client.post(f"/parts-requests/{parts.json()['id']}/approve", headers=AUTH)
    assert approved.status_code == 200, approved.text
    assert approved.json()["actor_kind"] == "human"
    assert approved.json()["request_id"] == parts.json()["id"]
    assert _balance(client, member["id"]) == before

    login_member(client, "ada@example.com")
    crib = client.post(
        "/member/tool-crib-exceptions",
        json={"tool_code": "TC-FL-001", "reason": "Need it off the wall"},
    )
    assert crib.status_code == 201, crib.text
    denied = client.post(f"/tool-crib-exceptions/{crib.json()['id']}/deny", headers=AI)
    assert denied.status_code == 200, denied.text
    assert denied.json()["status"] == "denied"
    assert denied.json()["actor_kind"] == "ai"
    assert _balance(client, member["id"]) == before


def test_ai_can_finish_or_send_back_a_claimed_job(client: TestClient) -> None:
    member = create_member(client, email="ada@example.com")
    before = _balance(client, member["id"])
    job = client.post("/jobs", headers=AUTH, json={"title": "Sweep the floor", "token_bounty": "25"})
    assert job.status_code == 201, job.text
    login_member(client, "ada@example.com")
    claimed = client.post(f"/member/jobs/{job.json()['id']}/claim")
    assert claimed.status_code == 200, claimed.text
    assert claimed.json()["status"] == "claimed"

    done = client.post(f"/jobs/{job.json()['id']}/done", headers=AI)
    assert done.status_code == 200, done.text
    assert done.json()["status"] == "done"
    assert done.json()["action"] == "job_done"
    assert done.json()["actor_kind"] == "ai"
    assert done.json()["request_id"] == job.json()["id"]
    assert _balance(client, member["id"]) == before
    photos = client.post(f"/jobs/{job.json()['id']}/photos", headers=AI)
    assert photos.status_code == 404

    other = client.post("/jobs", headers=AI, json={"title": "Empty the oil drum", "token_bounty": "40"})
    assert other.status_code == 201, other.text
    assert client.post(f"/member/jobs/{other.json()['id']}/claim").status_code == 200
    sent = client.post(f"/jobs/{other.json()['id']}/send-back", headers=AI)
    assert sent.status_code == 200, sent.text
    assert sent.json()["status"] == "sent_back"
    assert sent.json()["action"] == "job_send_back"
    assert _balance(client, member["id"]) == before


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


def test_claim_job_locks_the_job_row(client: TestClient, monkeypatch) -> None:
    """claim_job selects the shop job FOR UPDATE before the open check.

    Two claims in flight otherwise both read open, and the later commit
    wins, so the first member believes they hold the job. The second claim
    after the first commits is 400 job_not_open. An unknown job is 404.
    SQLite drops FOR UPDATE; this checks the statement still asks for the
    lock. Red on main: that job select has no FOR UPDATE.
    """
    ada = create_member(client, name="Ada Reyes", email="ada.claim-lock@example.com")
    create_member(client, name="Ben Cole", email="ben.claim-lock@example.com")
    created = client.post(
        "/jobs",
        headers=AUTH,
        json={"title": "Sweep the bay", "token_bounty": "25"},
    )
    assert created.status_code == 201, created.text
    job_id = created.json()["id"]

    login_member(client, "ada.claim-lock@example.com")
    reads: list[tuple[str, bool]] = []
    _record_scalars(monkeypatch, reads)
    first = client.post(f"/member/jobs/{job_id}/claim")
    claim_reads = list(reads)
    assert first.status_code == 200, first.text
    assert first.json()["status"] == "claimed"
    assert first.json()["claimed_by_member_id"] == ada["id"]

    login_member(client, "ben.claim-lock@example.com")
    second = client.post(f"/member/jobs/{job_id}/claim")
    assert second.status_code == 400, second.text
    assert second.json()["error"]["code"] == "job_not_open"

    missing = client.post(f"/member/jobs/{uuid4()}/claim")
    assert missing.status_code == 404, missing.text
    assert missing.json()["error"]["code"] == "not_found"
    assert missing.json()["error"]["message"] == "Job not found."

    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        row = session.get(ShopJob, UUID(job_id))
        assert row is not None
        assert row.status == ShopJobStatus.CLAIMED
        assert str(row.claimed_by_member_id) == ada["id"]
    finally:
        session.close()

    job_selects = [
        (sql, is_locked)
        for sql, is_locked in claim_reads
        if "FROM shop_jobs" in sql and "shop_jobs.id" in sql
    ]
    first_sql, first_locked = job_selects[0] if job_selects else ("", False)
    assert first_locked and "FOR UPDATE" in first_sql, (
        "claim job select has no FOR UPDATE on the postgresql dialect"
    )


def test_drafts_wait_for_accept(client: TestClient) -> None:
    member = create_member(client, email="ada@example.com")
    outbox_before = client.get("/fill/outbox", headers=AUTH)
    assert outbox_before.status_code == 200
    before_count = len(outbox_before.json())

    draft = client.post(
        "/fill/drafts",
        headers=AI,
        json={"body": "Tomorrow has open customer-bay hours."},
    )
    assert draft.status_code == 201, draft.text
    assert draft.json()["status"] == "draft"
    assert len(client.get("/fill/outbox", headers=AUTH).json()) == before_count
    own = client.post(f"/fill/drafts/{draft.json()['id']}/accept", headers=AI)
    assert own.status_code == 403
    assert own.json()["error"]["code"] == "cannot_approve_own_request"
    assert len(client.get("/fill/outbox", headers=AUTH).json()) == before_count

    accepted = client.post(f"/fill/drafts/{draft.json()['id']}/accept", headers=AUTH)
    assert accepted.status_code == 200, accepted.text
    assert accepted.json()["actor_kind"] == "human"
    assert accepted.json()["request_id"] == draft.json()["id"]
    assert len(client.get("/fill/outbox", headers=AUTH).json()) > before_count
    assert "shop is open" not in accepted.text.lower()

    room = client.post(
        "/chat/rooms",
        headers=AUTH,
        json={"title": "Ada", "member_ids": [member["id"]]},
    )
    assert room.status_code == 201, room.text
    chat_draft = client.post(
        "/chat/drafts",
        headers=AI,
        json={"room_id": room.json()["id"], "body": "The bay is yours after approval."},
    )
    assert chat_draft.status_code == 201, chat_draft.text
    messages = client.get(f"/chat/rooms/{room.json()['id']}/messages", headers=AUTH)
    assert messages.json()["messages"] == []
    direct = client.post(
        f"/chat/rooms/{room.json()['id']}/messages",
        headers=AI,
        json={"body": "This should stay a draft."},
    )
    assert direct.status_code == 403
    assert direct.json()["error"]["code"] == "draft_required"
    accepted_chat = client.post(f"/chat/drafts/{chat_draft.json()['id']}/accept", headers=AUTH)
    assert accepted_chat.status_code == 200, accepted_chat.text
    sent = client.get(f"/chat/rooms/{room.json()['id']}/messages", headers=AUTH).json()["messages"]
    assert len(sent) == 1
    assert sent[0]["body"] == "The bay is yours after approval."


def test_ai_reads_schedule_balance_and_open_requests(client: TestClient) -> None:
    member = create_member(client, email="ada@example.com")
    shop = create_hoist(client, name="Shop", is_shop=True)
    bay = create_hoist(client, name="Bay 1")
    start, end = _window(5)
    request = _request_hoist(client, "ada@example.com", shop["id"], start, end)
    booked = client.post(
        "/member/bookings",
        json={"hoist_id": bay["id"], "start_at": start, "end_at": end},
    )
    assert booked.status_code == 201, booked.text
    assert booked.json()["kind"] == "customer"

    schedule = client.get("/staff/schedule", headers=AI)
    assert schedule.status_code == 200, schedule.text
    assert [row["id"] for row in schedule.json()] == [booked.json()["id"]]
    human_schedule = client.get("/staff/schedule", headers=AUTH)
    assert [row["id"] for row in human_schedule.json()] == [booked.json()["id"]]

    balance = client.get(f"/staff/members/{member['id']}/balance", headers=AI)
    assert balance.status_code == 200, balance.text
    assert balance.json()["actor_kind"] == "ai"
    assert _dec(balance.json()["token_balance"]) == _balance(client, member["id"])

    parts = client.post(
        "/parts-requests",
        headers=AI,
        json={"member_id": member["id"], "sku": "PT-OIL-5W30-012"},
    )
    assert parts.status_code == 201, parts.text
    open_requests = client.get("/staff/requests", headers=AI)
    assert open_requests.status_code == 200, open_requests.text
    body = open_requests.json()
    assert body["actor_kind"] == "ai"
    assert [row["id"] for row in body["shop_hoist"]] == [request["id"]]
    assert [row["id"] for row in body["parts"]] == [parts.json()["id"]]
    human_open = client.get("/staff/requests", headers=AUTH)
    assert human_open.json()["actor_kind"] == "human"
    assert [row["id"] for row in human_open.json()["shop_hoist"]] == [request["id"]]


def test_ai_cannot_refund_charge_or_say_the_shop_is_open(client: TestClient) -> None:
    member = create_member(client, email="ada@example.com")
    bay = create_hoist(client, name="Bay 1")
    start, end = _window(4)
    before = _balance(client, member["id"])
    adjust = client.post(
        f"/members/{member['id']}/tokens",
        headers=AI,
        json={"amount": "10", "note": "no"},
    )
    assert adjust.status_code == 403
    assert adjust.json()["error"]["code"] == "token_change_requires_human"
    assert _balance(client, member["id"]) == before

    login_member(client, "ada@example.com")
    booked = client.post(
        "/member/bookings",
        json={"hoist_id": bay["id"], "start_at": start, "end_at": end},
    )
    assert booked.status_code == 201, booked.text
    reserved = _balance(client, member["id"])
    assert reserved < before
    cancel = client.post(f"/bookings/{booked.json()['id']}/cancel", headers=AI)
    assert cancel.status_code == 403
    assert cancel.json()["error"]["code"] == "refund_requires_human"
    assert _balance(client, member["id"]) == reserved

    refund = client.post("/refund-requests", headers=AI, json={"booking_id": booked.json()["id"]})
    assert refund.status_code == 201, refund.text
    ai_accept = client.post(f"/refund-requests/{refund.json()['id']}/accept", headers=AI)
    assert ai_accept.status_code == 403
    assert ai_accept.json()["error"]["code"] == "refund_requires_human"
    assert _balance(client, member["id"]) == reserved
    human_accept = client.post(f"/refund-requests/{refund.json()['id']}/accept", headers=AUTH)
    assert human_accept.status_code == 200, human_accept.text
    assert human_accept.json()["actor_kind"] == "human"
    assert human_accept.json()["request_id"] == refund.json()["id"]
    assert _balance(client, member["id"]) == before

    for path in ("/stripe", "/payments/charge", "/dns", "/worker", "/shop/open"):
        missing = client.post(path, headers=AI, json={})
        assert missing.status_code == 404
        assert "shop is open" not in missing.text.lower()


def test_accept_refund_on_checked_in_visit_does_not_cancel(client: TestClient) -> None:
    member = create_member(client, email="ada@example.com")
    bay = create_hoist(client, name="Bay 1")
    opening = _balance(client, member["id"])

    # Inside the check-in window so this visit can be checked in.
    active = _owner_booking(client, member["id"], bay["id"], minutes_from_now=10)
    assert client.post(f"/bookings/{active['id']}/confirm", headers=AUTH).status_code == 200
    checked = client.post(f"/bookings/{active['id']}/check-in", headers=AUTH)
    assert checked.status_code == 200, checked.text
    assert checked.json()["status"] == "active"
    reserved = _dec(checked.json()["reserved_tokens"])
    assert reserved > 0
    held = _balance(client, member["id"])
    assert held == opening - reserved
    ledger_before = _booking_ledger(client, member["id"], active["id"])
    assert [row["kind"] for row in ledger_before] == ["booking_reserve"]

    filed = client.post("/refund-requests", headers=AUTH, json={"booking_id": active["id"]})
    assert filed.status_code == 201, filed.text
    assert filed.json()["status"] == "pending"
    request_id = filed.json()["id"]

    ai_accept = client.post(f"/refund-requests/{request_id}/accept", headers=AI)
    assert ai_accept.status_code == 403
    assert ai_accept.json()["error"]["code"] == "refund_requires_human"
    assert _balance(client, member["id"]) == held
    assert [row["id"] for row in _booking_ledger(client, member["id"], active["id"])] == [
        row["id"] for row in ledger_before
    ]

    accepted = client.post(f"/refund-requests/{request_id}/accept", headers=AUTH)
    stored = _stored_booking(client, active["id"])
    ledger_after = _booking_ledger(client, member["id"], active["id"])
    refund_amounts = [row["amount"] for row in ledger_after if row["kind"] == "booking_refund"]
    request = _refund_request(client, request_id)
    payload = accepted.json()
    code = payload.get("error", {}).get("code")
    assert accepted.status_code == 409, (
        f"accept={accepted.status_code} code={code} booking={stored['status']} "
        f"reserve={stored['reserved_tokens']} was={reserved} "
        f"booking_refund={refund_amounts} request={request['status']} "
        f"ledger={len(ledger_after)} was={len(ledger_before)}"
    )
    error = payload["error"]
    assert set(error) == {"code", "message"}
    assert error["code"] == "refund_after_check_in"
    assert error["message"]
    assert stored["status"] == "active"
    assert _dec(stored["reserved_tokens"]) == reserved
    assert refund_amounts == []
    assert [row["id"] for row in ledger_after] == [row["id"] for row in ledger_before]
    assert request["status"] == "pending"
    assert request["decided_by_kind"] is None
    assert request["decided_at"] is None
    assert _balance(client, member["id"]) == held

    pending = _owner_booking(client, member["id"], bay["id"], 10)
    pending_reserved = _dec(pending["reserved_tokens"])
    pending_refund = client.post(
        "/refund-requests", headers=AUTH, json={"booking_id": pending["id"]}
    )
    assert pending_refund.status_code == 201, pending_refund.text
    pending_accept = client.post(
        f"/refund-requests/{pending_refund.json()['id']}/accept", headers=AUTH
    )
    assert pending_accept.status_code == 200, pending_accept.text
    pending_stored = _stored_booking(client, pending["id"])
    assert pending_stored["status"] == "cancelled"
    assert _dec(pending_stored["reserved_tokens"]) == Decimal("0")
    pending_rows = [
        row
        for row in _booking_ledger(client, member["id"], pending["id"])
        if row["kind"] == "booking_refund"
    ]
    assert len(pending_rows) == 1
    assert _dec(pending_rows[0]["amount"]) == pending_reserved
    again = client.post(
        f"/refund-requests/{pending_refund.json()['id']}/accept", headers=AUTH
    )
    assert again.status_code == 400
    assert again.json()["error"]["code"] == "invalid_transition"
    still_one = [
        row
        for row in _booking_ledger(client, member["id"], pending["id"])
        if row["kind"] == "booking_refund"
    ]
    assert len(still_one) == 1
    assert _dec(still_one[0]["amount"]) == pending_reserved
    assert _balance(client, member["id"]) == held
    still_active = _stored_booking(client, active["id"])
    assert still_active["status"] == "active"
    assert _dec(still_active["reserved_tokens"]) == reserved

    confirmed = _owner_booking(client, member["id"], bay["id"], 16)
    confirmed_reserved = _dec(confirmed["reserved_tokens"])
    assert client.post(f"/bookings/{confirmed['id']}/confirm", headers=AUTH).status_code == 200
    assert _stored_booking(client, confirmed["id"])["status"] == "confirmed"
    confirmed_refund = client.post(
        "/refund-requests", headers=AUTH, json={"booking_id": confirmed["id"]}
    )
    assert confirmed_refund.status_code == 201, confirmed_refund.text
    confirmed_accept = client.post(
        f"/refund-requests/{confirmed_refund.json()['id']}/accept", headers=AUTH
    )
    assert confirmed_accept.status_code == 200, confirmed_accept.text
    confirmed_stored = _stored_booking(client, confirmed["id"])
    assert confirmed_stored["status"] == "cancelled"
    assert _dec(confirmed_stored["reserved_tokens"]) == Decimal("0")
    confirmed_rows = [
        row
        for row in _booking_ledger(client, member["id"], confirmed["id"])
        if row["kind"] == "booking_refund"
    ]
    assert len(confirmed_rows) == 1
    assert _dec(confirmed_rows[0]["amount"]) == confirmed_reserved
    assert _balance(client, member["id"]) == held
    untouched = _stored_booking(client, active["id"])
    assert untouched["status"] == "active"
    assert _dec(untouched["reserved_tokens"]) == reserved
    assert [
        row["kind"] for row in _booking_ledger(client, member["id"], active["id"])
    ] == ["booking_reserve"]
    assert _refund_request(client, request_id)["status"] == "pending"


def _assert_refund_refused(client: TestClient, booking_id: str, code: str) -> None:
    refused = client.post("/refund-requests", headers=AUTH, json={"booking_id": booking_id})
    assert refused.status_code == 409, refused.text
    assert refused.json()["error"]["code"] == code
    assert set(refused.json()["error"]) == {"code", "message"}


def test_refund_request_on_completed_booking_stores_nothing(client: TestClient) -> None:
    member = create_member(client, email="ada@example.com")
    bay = create_hoist(client, name="Bay 1")
    # Inside the check-in window so this visit can be checked in, then completed.
    booking = _owner_booking(client, member["id"], bay["id"], minutes_from_now=10)
    assert client.post(f"/bookings/{booking['id']}/confirm", headers=AUTH).status_code == 200
    checked = client.post(f"/bookings/{booking['id']}/check-in", headers=AUTH)
    assert checked.status_code == 200, checked.text
    completed = client.post(
        f"/bookings/{booking['id']}/complete",
        headers=AUTH,
        json={"unused_tokens": "0"},
    )
    assert completed.status_code == 200, completed.text
    assert completed.json()["status"] == "completed"

    _assert_refund_refused(client, booking["id"], "refund_not_open")
    assert _refund_ids(client, booking["id"]) == []
    assert _stored_booking(client, booking["id"])["status"] == "completed"


def test_refund_request_on_cancelled_booking_stores_nothing(client: TestClient) -> None:
    member = create_member(client, email="ada@example.com")
    bay = create_hoist(client, name="Bay 1")
    booking = _owner_booking(client, member["id"], bay["id"], 5)
    cancelled = client.post(f"/bookings/{booking['id']}/cancel", headers=AUTH)
    assert cancelled.status_code == 200, cancelled.text
    assert cancelled.json()["status"] == "cancelled"

    _assert_refund_refused(client, booking["id"], "refund_not_open")
    assert _refund_ids(client, booking["id"]) == []
    assert _stored_booking(client, booking["id"])["status"] == "cancelled"


def test_refund_request_on_overdue_booking_stores_nothing(client: TestClient) -> None:
    member = create_member(client, email="ada@example.com")
    bay = create_hoist(client, name="Bay 1")
    # Inside the check-in window. The visit is moved into the past before overdue.
    booking = _owner_booking(client, member["id"], bay["id"], minutes_from_now=10)
    assert client.post(f"/bookings/{booking['id']}/confirm", headers=AUTH).status_code == 200
    checked = client.post(f"/bookings/{booking['id']}/check-in", headers=AUTH)
    assert checked.status_code == 200, checked.text
    _move_into_the_past(client, booking["id"])
    overdue = client.post(f"/bookings/{booking['id']}/overdue", headers=AUTH)
    assert overdue.status_code == 200, overdue.text
    assert overdue.json()["status"] == "overdue"

    _assert_refund_refused(client, booking["id"], "refund_not_open")
    assert _refund_ids(client, booking["id"]) == []
    assert _stored_booking(client, booking["id"])["status"] == "overdue"


def test_second_refund_request_on_pending_booking_stores_nothing(client: TestClient) -> None:
    member = create_member(client, email="ada@example.com")
    bay = create_hoist(client, name="Bay 1")
    booking = _owner_booking(client, member["id"], bay["id"], 7)
    first = client.post("/refund-requests", headers=AUTH, json={"booking_id": booking["id"]})
    assert first.status_code == 201, first.text

    _assert_refund_refused(client, booking["id"], "refund_already_pending")
    assert _refund_ids(client, booking["id"]) == [(first.json()["id"], "pending")]
    assert _stored_booking(client, booking["id"])["status"] == "pending"


def test_refund_request_on_pending_confirmed_or_active_is_created(client: TestClient) -> None:
    bay = create_hoist(client, name="Bay 1")
    # Active starts 10 minutes out so check-in is inside the window. The other
    # two are not checked in and stay hours apart on this bay.
    for email, hours_from_now, minutes_from_now, status in (
        ("ada@example.com", 4, 0, "pending"),
        ("sam@example.com", 8, 0, "confirmed"),
        ("riley@example.com", 0, 10, "active"),
    ):
        member = create_member(client, email=email)
        booking = _owner_booking(
            client,
            member["id"],
            bay["id"],
            hours_from_now,
            minutes_from_now=minutes_from_now,
        )
        if status in ("confirmed", "active"):
            assert client.post(f"/bookings/{booking['id']}/confirm", headers=AUTH).status_code == 200
        if status == "active":
            checked = client.post(f"/bookings/{booking['id']}/check-in", headers=AUTH)
            assert checked.status_code == 200, checked.text
            assert checked.json()["status"] == "active"
        created = client.post("/refund-requests", headers=AUTH, json={"booking_id": booking["id"]})
        assert created.status_code == 201, created.text
        assert _refund_ids(client, booking["id"]) == [(created.json()["id"], "pending")]


_VISIT_CLOSED_NOTE = (
    "A completed, cancelled, or overdue visit is closed. This refund request is denied."
)


def _checked_in_with_refund(client: TestClient, email: str) -> tuple[dict, dict, str]:
    member = create_member(client, email=email)
    bay = create_hoist(client, name="Bay 1")
    booking = _owner_booking(client, member["id"], bay["id"], minutes_from_now=10)
    assert client.post(f"/bookings/{booking['id']}/confirm", headers=AUTH).status_code == 200
    checked = client.post(f"/bookings/{booking['id']}/check-in", headers=AUTH)
    assert checked.status_code == 200, checked.text
    assert checked.json()["status"] == "active"
    filed = client.post("/refund-requests", headers=AUTH, json={"booking_id": booking["id"]})
    assert filed.status_code == 201, filed.text
    assert filed.json()["status"] == "pending"
    return member, booking, filed.json()["id"]


def _refund_actions(client: TestClient, request_id: str) -> list[tuple[str, str]]:
    """(action, actor_kind) for this request, with no created_at or id order.

    SQLite now() is whole seconds, so the draft row and the deny row share a
    timestamp, and uuid4 is not insert order.
    """
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        rows = session.scalars(
            select(StaffAction).where(StaffAction.request_id == UUID(request_id))
        ).all()
        return [(row.action, row.actor_kind.value) for row in rows]
    finally:
        session.close()


def _assert_closed_visit_accept_denies(
    client: TestClient,
    *,
    member_id: str,
    booking_id: str,
    request_id: str,
    booking_status: str,
) -> None:
    ledger_before = _booking_ledger(client, member_id, booking_id)
    balance_before = _balance(client, member_id)
    reserved_before = _dec(_stored_booking(client, booking_id)["reserved_tokens"])
    accepted = client.post(f"/refund-requests/{request_id}/accept", headers=AUTH)
    stored = _stored_booking(client, booking_id)
    request = _refund_request(client, request_id)
    ledger_after = _booking_ledger(client, member_id, booking_id)
    payload = accepted.json()
    code = payload.get("error", {}).get("code")
    assert accepted.status_code == 409, (
        f"accept={accepted.status_code} code={code} booking={stored['status']} "
        f"request={request['status']} ledger={len(ledger_after)} was={len(ledger_before)}"
    )
    error = payload["error"]
    assert set(error) == {"code", "message"}
    assert error["code"] == "refund_visit_closed"
    assert error["message"] == _VISIT_CLOSED_NOTE
    # RefundRequest.status is ShopHoistRequestStatus. The decline is stored as denied.
    assert request["status"] == "denied"
    assert request["decided_by_kind"] == "human"
    assert request["decided_at"] is not None
    assert stored["status"] == booking_status
    assert _dec(stored["reserved_tokens"]) == reserved_before
    assert {row["id"] for row in ledger_after} == {row["id"] for row in ledger_before}
    assert len(ledger_after) == len(ledger_before)
    assert _balance(client, member_id) == balance_before
    actions = _refund_actions(client, request_id)
    assert sorted(action for action, _actor in actions) == ["deny", "draft"]
    assert ("deny", "human") in actions
    again = client.post(f"/refund-requests/{request_id}/accept", headers=AUTH)
    assert again.status_code == 400
    assert again.json()["error"]["code"] == "invalid_transition"
    assert _refund_request(client, request_id)["status"] == "denied"
    assert {row["id"] for row in _booking_ledger(client, member_id, booking_id)} == {
        row["id"] for row in ledger_before
    }
    assert sorted(action for action, _actor in _refund_actions(client, request_id)) == [
        "deny",
        "draft",
    ]


def test_accept_refund_after_complete_denies_the_request(client: TestClient) -> None:
    member, booking, request_id = _checked_in_with_refund(client, "ada@example.com")
    completed = client.post(
        f"/bookings/{booking['id']}/complete",
        headers=AUTH,
        json={"unused_tokens": "0"},
    )
    assert completed.status_code == 200, completed.text
    assert completed.json()["status"] == "completed"

    # AI refusal still runs first and writes nothing. The request stays pending.
    ledger_before_ai = _booking_ledger(client, member["id"], booking["id"])
    ai_accept = client.post(f"/refund-requests/{request_id}/accept", headers=AI)
    assert ai_accept.status_code == 403
    assert ai_accept.json()["error"]["code"] == "refund_requires_human"
    ai_request = _refund_request(client, request_id)
    assert ai_request["status"] == "pending"
    assert ai_request["decided_by_kind"] is None
    assert sorted(action for action, _actor in _refund_actions(client, request_id)) == ["draft"]
    assert {row["id"] for row in _booking_ledger(client, member["id"], booking["id"])} == {
        row["id"] for row in ledger_before_ai
    }

    _assert_closed_visit_accept_denies(
        client,
        member_id=member["id"],
        booking_id=booking["id"],
        request_id=request_id,
        booking_status="completed",
    )


def test_accept_refund_after_overdue_denies_the_request(client: TestClient) -> None:
    member, booking, request_id = _checked_in_with_refund(client, "ada@example.com")
    _move_into_the_past(client, booking["id"])
    # POST /bookings/{id}/overdue calls mark_overdue.
    overdue = client.post(f"/bookings/{booking['id']}/overdue", headers=AUTH)
    assert overdue.status_code == 200, overdue.text
    assert overdue.json()["status"] == "overdue"
    _assert_closed_visit_accept_denies(
        client,
        member_id=member["id"],
        booking_id=booking["id"],
        request_id=request_id,
        booking_status="overdue",
    )


def test_accept_refund_after_cancel_denies_the_request(client: TestClient) -> None:
    # A checked-in visit is 400 cancel_after_check_in, so this case stays on a
    # confirmed visit. Accept after that cancel still denies the request.
    member = create_member(client, email="ada@example.com")
    bay = create_hoist(client, name="Bay 1")
    booking = _owner_booking(client, member["id"], bay["id"], hours_from_now=6)
    assert client.post(f"/bookings/{booking['id']}/confirm", headers=AUTH).status_code == 200
    filed = client.post("/refund-requests", headers=AUTH, json={"booking_id": booking["id"]})
    assert filed.status_code == 201, filed.text
    request_id = filed.json()["id"]
    cancelled = client.post(f"/bookings/{booking['id']}/cancel", headers=AUTH)
    assert cancelled.status_code == 200, cancelled.text
    assert cancelled.json()["status"] == "cancelled"
    _assert_closed_visit_accept_denies(
        client,
        member_id=member["id"],
        booking_id=booking["id"],
        request_id=request_id,
        booking_status="cancelled",
    )
