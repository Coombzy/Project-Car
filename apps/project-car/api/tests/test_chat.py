from __future__ import annotations

from fastapi.testclient import TestClient
from sqlalchemy.dialects import sqlite
from sqlalchemy.orm import Session

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
    assert blank.status_code == 400
    assert blank.json()["error"]["code"] == "empty_message"


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
