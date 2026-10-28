from __future__ import annotations

from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.dialects import sqlite
from sqlalchemy.orm import Session

from app.models import ChatMessage, ChatParticipant, ChatRoom
from tests.conftest import AUTH, create_member, login_member


def _create_room(client: TestClient, title: str, member_ids: list[str]) -> dict:
    response = client.post(
        "/chat/rooms",
        headers=AUTH,
        json={"title": title, "member_ids": member_ids},
    )
    assert response.status_code == 201, response.text
    return response.json()


def test_owner_creates_lists_mutes_and_posts(client: TestClient) -> None:
    ada = create_member(client, email="ada@example.com")
    denied = client.get("/chat/rooms")
    assert denied.status_code == 401

    room = _create_room(client, "Ada — turbo", [ada["id"]])
    assert room["title"] == "Ada — turbo"
    assert room["muted"] is False
    assert [row["email"] for row in room["participants"]] == ["ada@example.com"]
    assert room["last_message"] is None

    listed = client.get("/chat/rooms", headers=AUTH)
    assert listed.status_code == 200
    assert [row["id"] for row in listed.json()] == [room["id"]]

    posted = client.post(
        f"/chat/rooms/{room['id']}/messages",
        headers=AUTH,
        json={"body": "Bring the turbo kit this afternoon."},
    )
    assert posted.status_code == 201, posted.text
    body = posted.json()
    assert body["sender_role"] == "owner"
    assert body["sender_name"] == "Owner"
    assert body["body"] == "Bring the turbo kit this afternoon."

    page = client.get(f"/chat/rooms/{room['id']}/messages", headers=AUTH)
    assert page.status_code == 200
    messages = page.json()["messages"]
    assert len(messages) == 1
    assert messages[0]["id"] == body["id"]
    assert page.json()["cursor"] == body["id"]

    newer = client.get(
        f"/chat/rooms/{room['id']}/messages",
        headers=AUTH,
        params={"after_id": body["id"]},
    )
    assert newer.status_code == 200
    assert newer.json()["messages"] == []
    assert newer.json()["cursor"] == body["id"]

    muted = client.post(
        f"/chat/rooms/{room['id']}/mute",
        headers=AUTH,
        json={"muted": True},
    )
    assert muted.status_code == 200
    assert muted.json()["muted"] is True


def test_owner_create_requires_existing_member(client: TestClient) -> None:
    missing = client.post(
        "/chat/rooms",
        headers=AUTH,
        json={"title": "Ghost", "member_ids": ["00000000-0000-4000-8000-000000000099"]},
    )
    assert missing.status_code == 400
    assert missing.json()["error"]["code"] == "unknown_member"

    empty = client.post("/chat/rooms", headers=AUTH, json={"title": "Nope", "member_ids": []})
    assert empty.status_code == 422


def test_member_lists_own_rooms_posts_and_polls(client: TestClient) -> None:
    ada = create_member(client, email="ada@example.com")
    casey = create_member(client, name="Casey", email="casey@example.com", tier_name="basic")
    ada_room = _create_room(client, "Ada — turbo", [ada["id"]])
    casey_room = _create_room(client, "Casey — brakes", [casey["id"]])
    client.post(
        f"/chat/rooms/{ada_room['id']}/messages",
        headers=AUTH,
        json={"body": "Ada, bay is confirmed."},
    )

    login_member(client, "ada@example.com")
    assert client.get("/chat/rooms").status_code == 401
    assert client.post(
        "/chat/rooms",
        json={"title": "Sneaky", "member_ids": [ada["id"]]},
    ).status_code == 401
    assert client.get(f"/member/chat/rooms/{casey_room['id']}").status_code == 404
    assert client.get(f"/member/chat/rooms/{casey_room['id']}/messages").status_code == 404

    own = client.get("/member/chat/rooms")
    assert own.status_code == 200, own.text
    titles = [row["title"] for row in own.json()]
    assert titles == ["Ada — turbo"]
    assert own.json()[0]["last_message"]["body"] == "Ada, bay is confirmed."

    sent = client.post(
        f"/member/chat/rooms/{ada_room['id']}/messages",
        json={"body": "On my way with the kit."},
    )
    assert sent.status_code == 201, sent.text
    assert sent.json()["sender_role"] == "member"
    assert sent.json()["sender_name"] == "Ada Reyes"

    page = client.get(f"/member/chat/rooms/{ada_room['id']}/messages")
    assert page.status_code == 200
    bodies = [row["body"] for row in page.json()["messages"]]
    assert bodies == ["Ada, bay is confirmed.", "On my way with the kit."]

    first_id = page.json()["messages"][0]["id"]
    polled = client.get(
        f"/member/chat/rooms/{ada_room['id']}/messages",
        params={"after_id": first_id},
    )
    assert polled.status_code == 200
    assert [row["body"] for row in polled.json()["messages"]] == ["On my way with the kit."]

    stolen = client.post(
        f"/member/chat/rooms/{casey_room['id']}/messages",
        json={"body": "Should not land."},
    )
    assert stolen.status_code == 404


def test_member_cannot_see_unrelated_owner_thread(client: TestClient) -> None:
    ada = create_member(client, email="ada@example.com")
    casey = create_member(client, name="Casey", email="casey@example.com", tier_name="basic")
    _create_room(client, "Casey only", [casey["id"]])
    login_member(client, "ada@example.com")
    listed = client.get("/member/chat/rooms")
    assert listed.status_code == 200
    assert listed.json() == []
    assert ada["email"] == "ada@example.com"


def test_empty_message_rejected(client: TestClient) -> None:
    ada = create_member(client, email="ada@example.com")
    room = _create_room(client, "Ada", [ada["id"]])
    blank = client.post(
        f"/chat/rooms/{room['id']}/messages",
        headers=AUTH,
        json={"body": "   "},
    )
    assert blank.status_code == 422, blank.text
    assert blank.json()["error"]["code"] == "validation_error"


def _count_rows(client: TestClient, model: type) -> int:
    session: Session = client.session_factory()  # type: ignore[attr-defined]
    try:
        return int(session.scalar(select(func.count()).select_from(model)) or 0)
    finally:
        session.close()


def _validation_types(response) -> list[str]:
    return [row["type"] for row in response.json()["error"]["details"]]


def test_owner_whitespace_message_is_422_and_stores_nothing(client: TestClient) -> None:
    ada = create_member(client, email="ada@example.com")
    room = _create_room(client, "Ada", [ada["id"]])
    before = _count_rows(client, ChatMessage)
    spaces = client.post(
        f"/chat/rooms/{room['id']}/messages",
        headers=AUTH,
        json={"body": "   "},
    )
    assert spaces.status_code == 422, spaces.text
    assert spaces.json()["error"]["code"] == "validation_error"
    empty = client.post(
        f"/chat/rooms/{room['id']}/messages",
        headers=AUTH,
        json={"body": ""},
    )
    assert empty.status_code == 422, empty.text
    assert _validation_types(spaces) == _validation_types(empty)
    page = client.get(f"/chat/rooms/{room['id']}/messages", headers=AUTH)
    assert page.status_code == 200, page.text
    assert page.json()["messages"] == []
    assert _count_rows(client, ChatMessage) == before

    posted = client.post(
        f"/chat/rooms/{room['id']}/messages",
        headers=AUTH,
        json={"body": "  Bring the kit  "},
    )
    assert posted.status_code == 201, posted.text
    assert posted.json()["body"] == "Bring the kit"
    assert _count_rows(client, ChatMessage) == before + 1

    too_long = client.post(
        f"/chat/rooms/{room['id']}/messages",
        headers=AUTH,
        json={"body": "x" * 4001},
    )
    assert too_long.status_code == 422, too_long.text
    padded = client.post(
        f"/chat/rooms/{room['id']}/messages",
        headers=AUTH,
        json={"body": " " + ("x" * 4000)},
    )
    assert padded.status_code == 422, padded.text
    assert _count_rows(client, ChatMessage) == before + 1


def test_member_whitespace_message_is_422(client: TestClient) -> None:
    ada = create_member(client, email="ada@example.com")
    room = _create_room(client, "Ada", [ada["id"]])
    login_member(client, "ada@example.com")
    before = _count_rows(client, ChatMessage)
    spaces = client.post(
        f"/member/chat/rooms/{room['id']}/messages",
        json={"body": "   "},
    )
    assert spaces.status_code == 422, spaces.text
    assert spaces.json()["error"]["code"] == "validation_error"
    empty = client.post(
        f"/member/chat/rooms/{room['id']}/messages",
        json={"body": ""},
    )
    assert empty.status_code == 422, empty.text
    assert _validation_types(spaces) == _validation_types(empty)
    assert _count_rows(client, ChatMessage) == before


def test_owner_whitespace_room_title_is_422(client: TestClient) -> None:
    ada = create_member(client, email="ada@example.com")
    before = _count_rows(client, ChatRoom)
    spaces = client.post(
        "/chat/rooms",
        headers=AUTH,
        json={"title": "  ", "member_ids": [ada["id"]]},
    )
    assert spaces.status_code == 422, spaces.text
    assert spaces.json()["error"]["code"] == "validation_error"
    empty = client.post(
        "/chat/rooms",
        headers=AUTH,
        json={"title": "", "member_ids": [ada["id"]]},
    )
    assert empty.status_code == 422, empty.text
    assert _validation_types(spaces) == _validation_types(empty)
    assert _count_rows(client, ChatRoom) == before

    created = _create_room(client, "  Ada — turbo  ", [ada["id"]])
    assert created["title"] == "Ada — turbo"
    assert _count_rows(client, ChatRoom) == before + 1

    too_long = client.post(
        "/chat/rooms",
        headers=AUTH,
        json={"title": "t" * 201, "member_ids": [ada["id"]]},
    )
    assert too_long.status_code == 422, too_long.text
    padded = client.post(
        "/chat/rooms",
        headers=AUTH,
        json={"title": " " + ("t" * 200), "member_ids": [ada["id"]]},
    )
    assert padded.status_code == 422, padded.text
    assert _count_rows(client, ChatRoom) == before + 1


def _message_selects(statements: list) -> list[tuple[str, int | None]]:
    compiled: list[tuple[str, int | None]] = []
    for statement in statements:
        sql = str(statement.compile(dialect=sqlite.dialect()))
        if "FROM chat_messages" not in sql:
            continue
        limit = getattr(statement, "_limit_clause", None)
        cap = getattr(limit, "effective_value", None) if limit is not None else None
        compiled.append((sql, cap if isinstance(cap, int) else None))
    return compiled


def _assert_message_selects_are_limited(statements: list, cap: int) -> list[tuple[str, int | None]]:
    selects = _message_selects(statements)
    assert selects, "expected a chat_messages SELECT"
    unlimited = [sql for sql, sql_cap in selects if sql_cap is None or "LIMIT" not in sql]
    assert not unlimited, f"the SELECT has no SQL LIMIT: {unlimited}"
    page = [sql for sql, sql_cap in selects if sql_cap == cap and "LIMIT" in sql]
    assert page, f"the SELECT has no SQL LIMIT at {cap}: {selects}"
    return selects


def test_chat_list_messages_limits_in_sql(client: TestClient, monkeypatch) -> None:
    ada = create_member(client, email="ada@example.com")
    room = _create_room(client, "Ada — thread", [ada["id"]])
    posted: list[dict] = []
    for index in range(1, 6):
        response = client.post(
            f"/chat/rooms/{room['id']}/messages",
            headers=AUTH,
            json={"body": f"Note {index}"},
        )
        assert response.status_code == 201, response.text
        posted.append(response.json())

    seen: list = []
    original = Session.scalars

    def spy(self, statement, *args, **kwargs):
        seen.append(statement)
        return original(self, statement, *args, **kwargs)

    monkeypatch.setattr(Session, "scalars", spy)

    page = client.get(
        f"/chat/rooms/{room['id']}/messages",
        headers=AUTH,
        params={"limit": 2},
    )
    assert page.status_code == 200, page.text
    assert [row["body"] for row in page.json()["messages"]] == ["Note 4", "Note 5"]
    assert page.json()["cursor"] == posted[4]["id"]
    _assert_message_selects_are_limited(seen, 2)

    seen.clear()
    polled = client.get(
        f"/chat/rooms/{room['id']}/messages",
        headers=AUTH,
        params={"after_id": posted[1]["id"], "limit": 2},
    )
    assert polled.status_code == 200, polled.text
    assert [row["body"] for row in polled.json()["messages"]] == ["Note 3", "Note 4"]
    assert polled.json()["cursor"] == posted[3]["id"]
    poll_sql = _assert_message_selects_are_limited(seen, 2)
    assert any(
        "chat_messages.seq > ?" in sql and "ORDER BY chat_messages.seq ASC" in sql
        for sql, sql_cap in poll_sql
        if sql_cap == 2
    ), poll_sql

    seen.clear()
    tail = client.get(
        f"/chat/rooms/{room['id']}/messages",
        headers=AUTH,
        params={"after_id": posted[4]["id"], "limit": 2},
    )
    assert tail.status_code == 200, tail.text
    assert tail.json()["messages"] == []
    assert tail.json()["cursor"] == posted[4]["id"]
    tail_sql = _assert_message_selects_are_limited(seen, 2)
    assert any(
        "chat_messages.seq > ?" in sql and "ORDER BY chat_messages.seq ASC" in sql
        for sql, sql_cap in tail_sql
        if sql_cap == 2
    ), tail_sql

    missing = client.get(
        f"/chat/rooms/{room['id']}/messages",
        headers=AUTH,
        params={"after_id": "00000000-0000-4000-8000-000000000099", "limit": 2},
    )
    assert missing.status_code == 404
    assert missing.json()["error"]["code"] == "not_found"


def test_muted_room_rejects_member_message(client: TestClient) -> None:
    ada = create_member(client, email="ada@example.com")
    room = _create_room(client, "Ada — turbo", [ada["id"]])
    history = client.post(
        f"/chat/rooms/{room['id']}/messages",
        headers=AUTH,
        json={"body": "History stays."},
    )
    assert history.status_code == 201, history.text
    history_id = history.json()["id"]

    muted = client.post(
        f"/chat/rooms/{room['id']}/mute",
        headers=AUTH,
        json={"muted": True},
    )
    assert muted.status_code == 200
    assert muted.json()["muted"] is True

    login_member(client, "ada@example.com")
    rejected = client.post(
        f"/member/chat/rooms/{room['id']}/messages",
        json={"body": "This should not land."},
    )
    assert rejected.status_code == 403, rejected.text
    assert rejected.json()["error"]["code"] == "room_muted"

    stored = client.get(f"/member/chat/rooms/{room['id']}/messages")
    assert stored.status_code == 200
    assert [row["body"] for row in stored.json()["messages"]] == ["History stays."]

    owner_sent = client.post(
        f"/chat/rooms/{room['id']}/messages",
        headers=AUTH,
        json={"body": "Owner can still write."},
    )
    assert owner_sent.status_code == 201, owner_sent.text

    polled = client.get(
        f"/chat/rooms/{room['id']}/messages",
        headers=AUTH,
        params={"after_id": history_id},
    )
    assert polled.status_code == 200
    assert [row["body"] for row in polled.json()["messages"]] == ["Owner can still write."]
    assert polled.json()["cursor"] == owner_sent.json()["id"]

    unmuted = client.post(
        f"/chat/rooms/{room['id']}/mute",
        headers=AUTH,
        json={"muted": False},
    )
    assert unmuted.status_code == 200
    assert unmuted.json()["muted"] is False

    sent = client.post(
        f"/member/chat/rooms/{room['id']}/messages",
        json={"body": "Unmuted, I can reply."},
    )
    assert sent.status_code == 201, sent.text

    final = client.get(f"/member/chat/rooms/{room['id']}/messages")
    assert final.status_code == 200
    assert [row["body"] for row in final.json()["messages"]] == [
        "History stays.",
        "Owner can still write.",
        "Unmuted, I can reply.",
    ]


def _is_room_seq_max(statement: object) -> bool:
    sql = str(statement.compile(dialect=sqlite.dialect())).lower()  # type: ignore[attr-defined]
    return "max(" in sql and "chat_messages.seq" in sql


def _room_seqs(client: TestClient, room_id: str) -> list[int]:
    session: Session = client.session_factory()  # type: ignore[attr-defined]
    try:
        rows = session.scalars(
            select(ChatMessage.seq)
            .where(ChatMessage.room_id == UUID(room_id))
            .order_by(ChatMessage.seq.asc())
        ).all()
        return [int(seq) for seq in rows]
    finally:
        session.close()


def test_chat_post_retries_on_seq_collision(client: TestClient, monkeypatch) -> None:
    ada = create_member(client, email="ada@example.com")
    room = _create_room(client, "Ada — collision", [ada["id"]])
    first = client.post(
        f"/chat/rooms/{room['id']}/messages",
        headers=AUTH,
        json={"body": "Already stored."},
    )
    assert first.status_code == 201, first.text

    original = Session.scalar
    max_reads = {"n": 0}

    def first_max_is_already_taken(self, statement, *args, **kwargs):
        if _is_room_seq_max(statement):
            max_reads["n"] += 1
            # Seq 1 is stored. A stale max of 0 makes this post allocate 1 again.
            if max_reads["n"] == 1:
                return 0
        return original(self, statement, *args, **kwargs)

    monkeypatch.setattr(Session, "scalar", first_max_is_already_taken)

    posted = client.post(
        f"/chat/rooms/{room['id']}/messages",
        headers=AUTH,
        json={"body": "Landed after the collision."},
    )
    assert posted.status_code == 201, posted.text
    assert max_reads["n"] == 2

    page = client.get(f"/chat/rooms/{room['id']}/messages", headers=AUTH)
    assert page.status_code == 200, page.text
    assert [row["body"] for row in page.json()["messages"]] == [
        "Already stored.",
        "Landed after the collision.",
    ]
    assert _room_seqs(client, room["id"]) == [1, 2]

    busy_reads = {"n": 0}

    def every_max_is_already_taken(self, statement, *args, **kwargs):
        if _is_room_seq_max(statement):
            busy_reads["n"] += 1
            return 0
        return original(self, statement, *args, **kwargs)

    monkeypatch.setattr(Session, "scalar", every_max_is_already_taken)
    busy = client.post(
        f"/chat/rooms/{room['id']}/messages",
        headers=AUTH,
        json={"body": "Should not land."},
    )
    assert busy.status_code == 409, busy.text
    assert busy.json()["error"]["code"] == "chat_busy"
    assert busy_reads["n"] == 3

    kept = client.get(f"/chat/rooms/{room['id']}/messages", headers=AUTH)
    assert kept.status_code == 200, kept.text
    assert [row["body"] for row in kept.json()["messages"]] == [
        "Already stored.",
        "Landed after the collision.",
    ]
    assert _room_seqs(client, room["id"]) == [1, 2]


_INACTIVE_ROOM_MESSAGE = "Only active members can be added to a chat room."


def _chat_counts(client: TestClient) -> tuple[int, int, int]:
    # A seeded database already has demo threads, so compare with the count before the call.
    return (
        _count_rows(client, ChatRoom),
        _count_rows(client, ChatParticipant),
        _count_rows(client, ChatMessage),
    )


def _assert_room_refused(response, before: tuple[int, int, int], client: TestClient) -> None:
    assert response.status_code == 400, response.text
    assert response.json()["error"]["code"] == "member_not_active"
    assert response.json()["error"]["message"] == _INACTIVE_ROOM_MESSAGE
    assert _chat_counts(client) == before


@pytest.mark.parametrize("status", ["suspended", "banned", "churned"])
def test_owner_create_room_rejects_inactive_member(client: TestClient, status: str) -> None:
    ada = create_member(client, email="ada@example.com")
    patched = client.patch(f"/members/{ada['id']}", headers=AUTH, json={"status": status})
    assert patched.status_code == 200, patched.text
    assert patched.json()["status"] == status
    before = _chat_counts(client)
    denied = client.post(
        "/chat/rooms",
        headers=AUTH,
        json={"title": "Closed", "member_ids": [ada["id"]]},
    )
    _assert_room_refused(denied, before, client)


def test_owner_create_room_with_one_banned_member_writes_nothing(client: TestClient) -> None:
    ada = create_member(client, email="ada@example.com")
    casey = create_member(client, name="Casey", email="casey@example.com", tier_name="basic")
    patched = client.patch(f"/members/{casey['id']}", headers=AUTH, json={"status": "banned"})
    assert patched.status_code == 200, patched.text
    before = _chat_counts(client)
    denied = client.post(
        "/chat/rooms",
        headers=AUTH,
        json={"title": "Ada and Casey", "member_ids": [ada["id"], casey["id"]]},
    )
    _assert_room_refused(denied, before, client)


def test_owner_create_room_with_active_members_is_201(client: TestClient) -> None:
    ada = create_member(client, email="ada@example.com")
    casey = create_member(client, name="Casey", email="casey@example.com", tier_name="basic")
    before_rooms, before_participants, before_messages = _chat_counts(client)
    room = _create_room(client, "Ada and Casey", [casey["id"], ada["id"]])
    assert room["title"] == "Ada and Casey"
    assert [(row["name"], row["email"]) for row in room["participants"]] == [
        ("Ada Reyes", "ada@example.com"),
        ("Casey", "casey@example.com"),
    ]
    rooms, participants, messages = _chat_counts(client)
    assert rooms == before_rooms + 1
    assert participants == before_participants + 2
    assert messages == before_messages
