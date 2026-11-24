from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.orm import Session

from app.models import ChatMessage, ChatParticipant, ChatRoom, ChatSenderRole
from app.services.chat import last_messages_for, list_rooms
from tests.conftest import AUTH, create_member


def _seed_rooms(client: TestClient, count: int) -> dict[UUID, str]:
    member = create_member(client, email=f"list-{uuid4().hex[:8]}@example.com")
    member_id = UUID(member["id"])
    session: Session = client.session_factory()  # type: ignore[attr-defined]
    expected: dict[UUID, str] = {}
    now = datetime.now(timezone.utc)
    for i in range(count):
        room_id = uuid4()
        session.add(
            ChatRoom(
                id=room_id,
                title=f"Room {i:02d}",
                created_by_email="owner@example.com",
                muted=False,
                updated_at=now,
            )
        )
        session.add(ChatParticipant(room_id=room_id, member_id=member_id))
        session.add(
            ChatMessage(
                room_id=room_id,
                sender_role=ChatSenderRole.OWNER,
                sender_email="owner@example.com",
                sender_name="Owner",
                body=f"older-{i:02d}",
                seq=1,
            )
        )
        last_body = f"last-{i:02d}"
        session.add(
            ChatMessage(
                room_id=room_id,
                sender_role=ChatSenderRole.OWNER,
                sender_email="owner@example.com",
                sender_name="Owner",
                body=last_body,
                seq=2,
            )
        )
        expected[room_id] = last_body
    session.commit()
    session.close()
    return expected

def test_listing_50_rooms_issues_at_most_3_queries(client: TestClient) -> None:
    expected = _seed_rooms(client, 50)
    session: Session = client.session_factory()  # type: ignore[attr-defined]
    statements: list[str] = []

    def _count(conn, cursor, statement, parameters, context, executemany) -> None:
        statements.append(statement)

    event.listen(session.get_bind(), "before_cursor_execute", _count)
    try:
        rooms = list_rooms(session, limit=100)
        found = last_messages_for(session, [room.id for room in rooms])
    finally:
        event.remove(session.get_bind(), "before_cursor_execute", _count)
        session.close()

    assert len(statements) <= 3
    assert len(rooms) == 50
    assert {room.id: found[room.id].body for room in rooms} == expected

    listed = client.get("/chat/rooms", headers=AUTH)
    assert listed.status_code == 200
    body = listed.json()
    assert {UUID(row["id"]): row["last_message"]["body"] for row in body} == expected


def test_list_rooms_honors_limit(client: TestClient) -> None:
    _seed_rooms(client, 3)
    listed = client.get("/chat/rooms", headers=AUTH, params={"limit": 2})
    assert listed.status_code == 200
    assert len(listed.json()) == 2
