"""Owner/ops human chat: see-all rooms, create (Owner), mute, post, poll."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException, Query

from app.deps import DbSession, Owner
from app.schemas import (
    ChatMessageCreate,
    ChatMessageOut,
    ChatMessagePage,
    ChatMuteRequest,
    ChatRoomCreate,
    ChatRoomOut,
)
from app.services.chat import (
    ChatError,
    create_room,
    get_room,
    last_message_for,
    list_messages,
    list_rooms,
    post_message,
    set_muted,
)

router = APIRouter(prefix="/chat", tags=["chat"])


def _error(exc: ChatError) -> HTTPException:
    return HTTPException(status_code=exc.status, detail={"code": exc.code, "message": exc.message})


def _room_out(session, room) -> ChatRoomOut:
    last = last_message_for(session, room.id)
    return ChatRoomOut.from_room(room, last)


@router.get("/rooms", response_model=list[ChatRoomOut])
def owner_list_rooms(session: DbSession, _owner: Owner) -> list[ChatRoomOut]:
    return [_room_out(session, room) for room in list_rooms(session)]


@router.post("/rooms", response_model=ChatRoomOut, status_code=201)
def owner_create_room(body: ChatRoomCreate, session: DbSession, owner: Owner) -> ChatRoomOut:
    try:
        room = create_room(
            session,
            title=body.title,
            member_ids=body.member_ids,
            owner_email=owner.email,
        )
    except ChatError as exc:
        raise _error(exc) from exc
    return _room_out(session, room)


@router.get("/rooms/{room_id}", response_model=ChatRoomOut)
def owner_get_room(room_id: UUID, session: DbSession, _owner: Owner) -> ChatRoomOut:
    try:
        room = get_room(session, room_id)
    except ChatError as exc:
        raise _error(exc) from exc
    return _room_out(session, room)


@router.post("/rooms/{room_id}/mute", response_model=ChatRoomOut)
def owner_mute_room(
    room_id: UUID,
    body: ChatMuteRequest,
    session: DbSession,
    _owner: Owner,
) -> ChatRoomOut:
    try:
        room = set_muted(session, room_id, body.muted)
    except ChatError as exc:
        raise _error(exc) from exc
    return _room_out(session, room)


@router.get("/rooms/{room_id}/messages", response_model=ChatMessagePage)
def owner_list_messages(
    room_id: UUID,
    session: DbSession,
    _owner: Owner,
    after_id: UUID | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=200),
) -> ChatMessagePage:
    try:
        get_room(session, room_id)
        rows, cursor = list_messages(session, room_id, after_id=after_id, limit=limit)
    except ChatError as exc:
        raise _error(exc) from exc
    return ChatMessagePage(
        messages=[ChatMessageOut.model_validate(row) for row in rows],
        cursor=cursor,
    )


@router.post("/rooms/{room_id}/messages", response_model=ChatMessageOut, status_code=201)
def owner_post_message(
    room_id: UUID,
    body: ChatMessageCreate,
    session: DbSession,
    owner: Owner,
) -> ChatMessageOut:
    try:
        room = get_room(session, room_id)
        row = post_message(session, room, principal=owner, body=body.body)
    except ChatError as exc:
        raise _error(exc) from exc
    return ChatMessageOut.model_validate(row)
