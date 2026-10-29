"""Owner incident log.

POST /incidents stores one row. GET /incidents lists newest first.
This router does not write a token ledger row and does not file from overdue.
The incidents table already exists (initial shop domain). No new revision.
"""

from __future__ import annotations

import threading
from datetime import datetime, timedelta, timezone
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Cookie, Depends, Header, HTTPException, Query
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import select

from app.auth import Principal
from app.config import Settings
from app.deps import DbSession, current_settings, require_member, require_owner
from app.models import Booking, Incident, IncidentKind, IncidentSeverity, Member

router = APIRouter(tags=["incidents"])

# Same page cap as GET /member/tokens.
_LIMIT_DEFAULT = 200
_LIMIT_MAX = 500

_created_lock = threading.Lock()
_last_created_at: datetime | None = None


def _created_at() -> datetime:
    """App stamp. SQLite now() is whole seconds, so two inserts would tie."""
    global _last_created_at
    with _created_lock:
        now = datetime.now(timezone.utc)
        if _last_created_at is not None and now <= _last_created_at:
            now = _last_created_at + timedelta(microseconds=1)
        _last_created_at = now
        return now


def require_incident_owner(
    settings: Annotated[Settings, Depends(current_settings)],
    session: DbSession,
    authorization: Annotated[str | None, Header()] = None,
    session_cookie: Annotated[str | None, Cookie(alias="pc_owner_session")] = None,
    member_session_cookie: Annotated[str | None, Cookie(alias="pc_member_session")] = None,
) -> Principal:
    """Owner cookie or bearer. A member session is 403, not a silent 401."""
    try:
        return require_owner(settings, authorization, session_cookie)
    except HTTPException as exc:
        if exc.status_code != 401:
            raise
    try:
        require_member(settings, session, member_session_cookie)
    except HTTPException as exc:
        if exc.status_code == 403:
            raise HTTPException(
                status_code=403,
                detail={"code": "forbidden", "message": "Incidents are Owner only."},
            ) from exc
        if exc.status_code != 401:
            raise
        raise HTTPException(
            status_code=401,
            detail={"code": "unauthorized", "message": "Owner authentication required."},
        ) from exc
    raise HTTPException(
        status_code=403,
        detail={"code": "forbidden", "message": "Incidents are Owner only."},
    )


IncidentOwner = Annotated[Principal, Depends(require_incident_owner)]


class IncidentCreate(BaseModel):
    kind: IncidentKind
    member_id: UUID | None = None
    booking_id: UUID | None = None
    note: str = Field(min_length=1, max_length=2000)

    @field_validator("note", mode="before")
    @classmethod
    def blank_note(cls, value: object) -> object:
        if isinstance(value, str) and not value.strip():
            return ""
        return value

    @field_validator("note")
    @classmethod
    def strip_note(cls, value: str) -> str:
        return value.strip()


class IncidentOut(BaseModel):
    id: UUID
    kind: IncidentKind
    member_id: UUID | None
    booking_id: UUID | None
    note: str
    created_at: datetime

    @classmethod
    def from_row(cls, row: Incident) -> IncidentOut:
        return cls(
            id=row.id,
            kind=row.kind,
            member_id=row.member_id,
            booking_id=row.booking_id,
            note=row.description,
            created_at=row.created_at,
        )


def _not_found(message: str) -> HTTPException:
    return HTTPException(status_code=404, detail={"code": "not_found", "message": message})


@router.post("/incidents", response_model=IncidentOut, status_code=201)
def create_incident(body: IncidentCreate, session: DbSession, _owner: IncidentOwner) -> IncidentOut:
    if body.member_id is not None and session.get(Member, body.member_id) is None:
        raise _not_found("Member not found.")
    if body.booking_id is not None and session.get(Booking, body.booking_id) is None:
        raise _not_found("Booking not found.")
    row = Incident(
        member_id=body.member_id,
        booking_id=body.booking_id,
        kind=body.kind,
        severity=IncidentSeverity.MINOR,
        description=body.note,
        photos=[],
        created_at=_created_at(),
    )
    session.add(row)
    session.flush()
    return IncidentOut.from_row(row)


@router.get("/incidents", response_model=list[IncidentOut])
def list_incidents(
    session: DbSession,
    _owner: IncidentOwner,
    limit: int = Query(default=_LIMIT_DEFAULT, ge=1, le=_LIMIT_MAX),
    offset: int = Query(default=0, ge=0),
) -> list[IncidentOut]:
    rows = session.scalars(
        select(Incident)
        .order_by(Incident.created_at.desc(), Incident.id.desc())
        .limit(limit)
        .offset(offset)
    ).all()
    return [IncidentOut.from_row(row) for row in rows]
