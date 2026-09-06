from __future__ import annotations

from fastapi.testclient import TestClient

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
