"""Human shop chat. Polling only — no Matrix, Apex, or Grok bridge."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.auth import Principal
from app.models import (
    ChatMessage,
    ChatParticipant,
    ChatRoom,
    ChatSenderRole,
    Member,
    MemberStatus,
)


class ChatError(Exception):
    def __init__(self, status: int, code: str, message: str) -> None:
        self.status = status
        self.code = code
        self.message = message
        super().__init__(message)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def get_room(session: Session, room_id: UUID) -> ChatRoom:
    room = session.scalars(
        select(ChatRoom)
        .options(selectinload(ChatRoom.participants).selectinload(ChatParticipant.member))
        .where(ChatRoom.id == room_id)
    ).first()
    if room is None:
        raise ChatError(404, "not_found", "Chat room not found.")
    return room


def _member_in_room(room: ChatRoom, member_id: UUID) -> bool:
    return any(row.member_id == member_id for row in room.participants)


def require_member_room(session: Session, room_id: UUID, member_id: UUID) -> ChatRoom:
    room = get_room(session, room_id)
    if not _member_in_room(room, member_id):
        raise ChatError(404, "not_found", "Chat room not found.")
    return room


def last_message_for(session: Session, room_id: UUID) -> ChatMessage | None:
    return session.scalars(
        select(ChatMessage)
        .where(ChatMessage.room_id == room_id)
        .order_by(ChatMessage.created_at.desc())
        .limit(1)
    ).first()


def list_rooms(session: Session, *, member_id: UUID | None = None) -> list[ChatRoom]:
    stmt = select(ChatRoom).options(
        selectinload(ChatRoom.participants).selectinload(ChatParticipant.member)
    )
    if member_id is not None:
        stmt = stmt.join(ChatParticipant).where(ChatParticipant.member_id == member_id)
    return list(session.scalars(stmt.order_by(ChatRoom.updated_at.desc()).distinct()).all())


def create_room(
    session: Session,
    *,
    title: str,
    member_ids: list[UUID],
    owner_email: str,
) -> ChatRoom:
    cleaned = title.strip()
    if not cleaned:
        raise ChatError(400, "invalid_title", "Room title is required.")
    unique_ids = list(dict.fromkeys(member_ids))
    if not unique_ids:
        raise ChatError(400, "members_required", "Pick at least one member.")

    members = list(session.scalars(select(Member).where(Member.id.in_(unique_ids))).all())
    found = {row.id for row in members}
    missing = [str(item) for item in unique_ids if item not in found]
    if missing:
        raise ChatError(400, "unknown_member", "One or more members were not found.")

    room = ChatRoom(
        title=cleaned[:200],
        created_by_email=owner_email,
        muted=False,
        updated_at=_now(),
    )
    session.add(room)
    session.flush()
    for member in members:
        session.add(ChatParticipant(room_id=room.id, member_id=member.id))
    session.flush()
    return get_room(session, room.id)


def set_muted(session: Session, room_id: UUID, muted: bool) -> ChatRoom:
    room = get_room(session, room_id)
    room.muted = muted
    room.updated_at = _now()
    session.add(room)
    session.flush()
    return room


def list_messages(
    session: Session,
    room_id: UUID,
    *,
    after_id: UUID | None = None,
    limit: int = 100,
) -> tuple[list[ChatMessage], UUID | None]:
    if after_id is not None:
        after = session.get(ChatMessage, after_id)
        if after is None or after.room_id != room_id:
            raise ChatError(404, "not_found", "Cursor message not found.")
        rows = list(
            session.scalars(
                select(ChatMessage)
                .where(
                    ChatMessage.room_id == room_id,
                    ChatMessage.created_at > after.created_at,
                )
                .order_by(ChatMessage.created_at.asc())
                .limit(limit)
            ).all()
        )
        cursor = rows[-1].id if rows else after_id
        return rows, cursor

    newest = list(
        session.scalars(
            select(ChatMessage)
            .where(ChatMessage.room_id == room_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
        ).all()
    )
    rows = list(reversed(newest))
    cursor = rows[-1].id if rows else None
    return rows, cursor


def post_message(
    session: Session,
    room: ChatRoom,
    *,
    principal: Principal,
    body: str,
) -> ChatMessage:
    cleaned = body.strip()
    if not cleaned:
        raise ChatError(400, "empty_message", "Message body is required.")
    if len(cleaned) > 4000:
        raise ChatError(400, "message_too_long", "Message must be 4000 characters or fewer.")

    if principal.role == "member":
        if principal.member_id is None or not _member_in_room(room, principal.member_id):
            raise ChatError(404, "not_found", "Chat room not found.")
        member = session.get(Member, principal.member_id)
        if member is None or member.status != MemberStatus.ACTIVE:
            raise ChatError(403, "member_not_bookable", "Only active members can send chat.")
        sender_role = ChatSenderRole.MEMBER
        sender_member_id = member.id
        sender_email = member.email
        sender_name = member.name
    elif principal.role == "owner":
        sender_role = ChatSenderRole.OWNER
        sender_member_id = None
        sender_email = principal.email
        sender_name = "Owner"
    else:
        raise ChatError(403, "forbidden", "Only Owner or a room member can send.")

    row = ChatMessage(
        room_id=room.id,
        sender_role=sender_role,
        sender_member_id=sender_member_id,
        sender_email=sender_email,
        sender_name=sender_name,
        body=cleaned,
    )
    session.add(row)
    room.updated_at = _now()
    session.add(room)
    session.flush()
    session.refresh(row)
    return row
