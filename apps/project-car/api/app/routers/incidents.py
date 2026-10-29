"""Owner incident desk: file a row and list newest first.

No token ledger row, no billing row, and no filing from the overdue path.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import select

from app.auth import Principal
from app.deps import AnyPrincipal, DbSession
from app.models import Booking, Incident, IncidentKind, IncidentSeverity, Member

router = APIRouter(tags=["incidents"])


class IncidentCreate(BaseModel):
    kind: IncidentKind
    member_id: UUID | None = None
    booking_id: UUID | None = None
    note: str = Field(min_length=1, max_length=2000)

    @field_validator("note", mode="before")
    @classmethod
    def strip_note(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip()
        return value


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


def _forbidden() -> HTTPException:
    return HTTPException(
        status_code=403,
        detail={"code": "forbidden", "message": "Owner authentication required."},
    )


def _not_found(message: str) -> HTTPException:
    return HTTPException(status_code=404, detail={"code": "not_found", "message": message})


def _owner_only(principal: Principal) -> None:
    # require_owner's staff stub: human Owner or the AI bearer. A member is 403.
    if principal.role not in {"owner", "ai"}:
        raise _forbidden()


@router.post("/incidents", response_model=IncidentOut, status_code=201)
def create_incident(
    body: IncidentCreate, session: DbSession, principal: AnyPrincipal
) -> IncidentOut:
    _owner_only(principal)
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
        created_at=datetime.now(timezone.utc),
    )
    session.add(row)
    session.flush()
    return IncidentOut.from_row(row)


@router.get("/incidents", response_model=list[IncidentOut])
def list_incidents(
    session: DbSession,
    principal: AnyPrincipal,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[IncidentOut]:
    _owner_only(principal)
    rows = session.scalars(
        select(Incident)
        .order_by(Incident.created_at.desc(), Incident.id.desc())
        .limit(limit)
        .offset(offset)
    ).all()
    return [IncidentOut.from_row(row) for row in rows]
