"""Member human chat: own rooms only, reply, poll. Cannot start rooms."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException, Query

from app.deps import DbSession, MemberUser
from app.schemas import ChatMessageCreate, ChatMessageOut, ChatMessagePage, ChatRoomOut
from app.services.chat import (
    ChatError,
    last_message_for,
    list_messages,
    list_rooms,
    post_message,
    require_member_room,
)

router = APIRouter(prefix="/member/chat", tags=["member-chat"])


def _error(exc: ChatError) -> HTTPException:
    return HTTPException(status_code=exc.status, detail={"code": exc.code, "message": exc.message})


def _room_out(session, room) -> ChatRoomOut:
    last = last_message_for(session, room.id)
    return ChatRoomOut.from_room(room, last)


@router.get("/rooms", response_model=list[ChatRoomOut])
def member_list_rooms(session: DbSession, principal: MemberUser) -> list[ChatRoomOut]:
    assert principal.member_id is not None
    return [_room_out(session, room) for room in list_rooms(session, member_id=principal.member_id)]


@router.get("/rooms/{room_id}", response_model=ChatRoomOut)
def member_get_room(room_id: UUID, session: DbSession, principal: MemberUser) -> ChatRoomOut:
    assert principal.member_id is not None
    try:
        room = require_member_room(session, room_id, principal.member_id)
    except ChatError as exc:
        raise _error(exc) from exc
    return _room_out(session, room)


@router.get("/rooms/{room_id}/messages", response_model=ChatMessagePage)
def member_list_messages(
    room_id: UUID,
    session: DbSession,
    principal: MemberUser,
    after_id: UUID | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=200),
) -> ChatMessagePage:
    assert principal.member_id is not None
    try:
        require_member_room(session, room_id, principal.member_id)
        rows, cursor = list_messages(session, room_id, after_id=after_id, limit=limit)
    except ChatError as exc:
        raise _error(exc) from exc
    return ChatMessagePage(
        messages=[ChatMessageOut.model_validate(row) for row in rows],
        cursor=cursor,
    )


@router.post("/rooms/{room_id}/messages", response_model=ChatMessageOut, status_code=201)
def member_post_message(
    room_id: UUID,
    body: ChatMessageCreate,
    session: DbSession,
    principal: MemberUser,
) -> ChatMessageOut:
    assert principal.member_id is not None
    try:
        room = require_member_room(session, room_id, principal.member_id)
        row = post_message(session, room, principal=principal, body=body.body)
    except ChatError as exc:
        raise _error(exc) from exc
    return ChatMessageOut.model_validate(row)
