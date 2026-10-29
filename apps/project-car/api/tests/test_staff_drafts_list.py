"""GET /staff/drafts lists pending fill and chat drafts for an Owner.

The list is newest first and includes kind, body, room id, and the author
(`created_by_kind` / `created_by_id` on `StaffDraftOut`). `kind` keeps one
kind. Accepted drafts stay stored and drop out of the list. `limit` defaults
to 50 and must be 1..200.

A member session is not an Owner. `require_owner` answers 401 `unauthorized`,
the same refusal as other Owner routes.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi.testclient import TestClient

from app.config import get_settings
from app.models import DraftStatus, StaffDraft
from tests.conftest import AUTH, create_member, login_member

AI = {"Authorization": "Bearer dev-ai-secret"}
_BASE = datetime(2026, 3, 1, tzinfo=timezone.utc)


def _stamp_created_at(client: TestClient, stamps: list[tuple[str, datetime]]) -> None:
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        for draft_id, created_at in stamps:
            row = session.get(StaffDraft, UUID(draft_id))
            assert row is not None
            row.created_at = created_at
        session.commit()
    finally:
        session.close()


def _stored_status(client: TestClient, draft_id: str) -> DraftStatus:
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        row = session.get(StaffDraft, UUID(draft_id))
        assert row is not None
        return row.status
    finally:
        session.close()


def test_owner_lists_pending_fill_and_chat_drafts(client: TestClient) -> None:
    member = create_member(client, email="ada@example.com")
    room = client.post(
        "/chat/rooms",
        headers=AUTH,
        json={"title": "Ada", "member_ids": [member["id"]]},
    )
    assert room.status_code == 201, room.text
    room_id = room.json()["id"]

    fill = client.post(
        "/fill/drafts",
        headers=AI,
        json={"body": "Tomorrow has open customer-bay hours."},
    )
    assert fill.status_code == 201, fill.text
    chat = client.post(
        "/chat/drafts",
        headers=AI,
        json={"room_id": room_id, "body": "The bay is yours after approval."},
    )
    assert chat.status_code == 201, chat.text
    fill_id = fill.json()["id"]
    chat_id = chat.json()["id"]
    _stamp_created_at(
        client,
        [
            (fill_id, _BASE),
            (chat_id, _BASE + timedelta(minutes=5)),
        ],
    )

    listed = client.get("/staff/drafts", headers=AUTH)
    assert listed.status_code == 200, listed.text
    rows = listed.json()
    assert [row["id"] for row in rows] == [chat_id, fill_id]
    settings = get_settings()
    assert rows[0]["kind"] == "chat"
    assert rows[0]["status"] == "draft"
    assert rows[0]["body"] == "The bay is yours after approval."
    assert rows[0]["room_id"] == room_id
    assert rows[0]["created_by_kind"] == "ai"
    assert rows[0]["created_by_id"] == settings.ai_actor_id
    assert rows[1]["kind"] == "fill"
    assert rows[1]["status"] == "draft"
    assert rows[1]["body"] == "Tomorrow has open customer-bay hours."
    assert rows[1]["room_id"] is None
    assert rows[1]["created_by_kind"] == "ai"
    assert rows[1]["created_by_id"] == settings.ai_actor_id

    only_fill = client.get("/staff/drafts", headers=AUTH, params={"kind": "fill"})
    assert only_fill.status_code == 200, only_fill.text
    assert [row["id"] for row in only_fill.json()] == [fill_id]
    only_chat = client.get("/staff/drafts", headers=AUTH, params={"kind": "chat"})
    assert only_chat.status_code == 200, only_chat.text
    assert [row["id"] for row in only_chat.json()] == [chat_id]
    bad_kind = client.get("/staff/drafts", headers=AUTH, params={"kind": "refund"})
    assert bad_kind.status_code == 422
    assert bad_kind.json()["error"]["code"] == "validation_error"

    ai_listed = client.get("/staff/drafts", headers=AI)
    assert [row["id"] for row in ai_listed.json()] == [chat_id, fill_id]

    accepted_fill = client.post(f"/fill/drafts/{fill_id}/accept", headers=AUTH)
    assert accepted_fill.status_code == 200, accepted_fill.text
    assert _stored_status(client, fill_id) == DraftStatus.ACCEPTED
    after_fill = client.get("/staff/drafts", headers=AUTH)
    assert after_fill.status_code == 200, after_fill.text
    assert [row["id"] for row in after_fill.json()] == [chat_id]

    accepted_chat = client.post(f"/chat/drafts/{chat_id}/accept", headers=AUTH)
    assert accepted_chat.status_code == 200, accepted_chat.text
    assert _stored_status(client, chat_id) == DraftStatus.ACCEPTED
    sent = client.get(f"/chat/rooms/{room_id}/messages", headers=AUTH).json()["messages"]
    assert [row["body"] for row in sent] == ["The bay is yours after approval."]
    after_both = client.get("/staff/drafts", headers=AUTH)
    assert after_both.status_code == 200, after_both.text
    assert after_both.json() == []

    login_member(client, "ada@example.com")
    denied = client.get("/staff/drafts")
    assert denied.status_code == 401, denied.text
    assert denied.json()["error"]["code"] == "unauthorized"
    assert "Tomorrow has open" not in denied.text
    assert "after approval" not in denied.text

    still = client.get("/staff/drafts", headers=AUTH)
    assert still.status_code == 200, still.text
    assert still.json() == []


def test_draft_list_limit_defaults_to_50_and_caps_at_200(client: TestClient) -> None:
    create_member(client, email="ada@example.com")
    ids: list[str] = []
    for index in range(51):
        created = client.post(
            "/fill/drafts",
            headers=AUTH,
            json={"body": f"Fill notice {index:02d}"},
        )
        assert created.status_code == 201, created.text
        ids.append(created.json()["id"])
    _stamp_created_at(
        client,
        [(draft_id, _BASE + timedelta(minutes=index)) for index, draft_id in enumerate(ids)],
    )

    listed = client.get("/staff/drafts", headers=AUTH)
    assert listed.status_code == 200, listed.text
    assert [row["id"] for row in listed.json()] == list(reversed(ids[1:]))
    assert listed.json()[0]["body"] == "Fill notice 50"
    assert all(row["kind"] == "fill" and row["status"] == "draft" for row in listed.json())

    newest = client.get("/staff/drafts", headers=AUTH, params={"limit": 1})
    assert newest.status_code == 200, newest.text
    assert [row["body"] for row in newest.json()] == ["Fill notice 50"]

    wide = client.get("/staff/drafts", headers=AUTH, params={"limit": 200})
    assert wide.status_code == 200, wide.text
    assert [row["id"] for row in wide.json()] == list(reversed(ids))

    too_high = client.get("/staff/drafts", headers=AUTH, params={"limit": 201})
    assert too_high.status_code == 422
    assert too_high.json()["error"]["code"] == "validation_error"
    too_low = client.get("/staff/drafts", headers=AUTH, params={"limit": 0})
    assert too_low.status_code == 422
    assert too_low.json()["error"]["code"] == "validation_error"

    accepted = client.post(f"/fill/drafts/{ids[-1]}/accept", headers=AUTH)
    assert accepted.status_code == 200, accepted.text
    assert _stored_status(client, ids[-1]) == DraftStatus.ACCEPTED
    after = client.get("/staff/drafts", headers=AUTH)
    assert after.status_code == 200, after.text
    assert [row["id"] for row in after.json()] == list(reversed(ids[:-1]))
    assert ids[-1] not in [row["id"] for row in after.json()]
