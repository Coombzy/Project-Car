"""Approve and deny routes. A human and an AI use the same API."""

from __future__ import annotations

from datetime import timedelta
from decimal import Decimal

from fastapi.testclient import TestClient

from app.shop_time import shop_now
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
