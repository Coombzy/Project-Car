from __future__ import annotations

from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.deps import AppSettings, DbSession, Owner
from app.models import WaitlistEntry
from app.schemas import WaitlistCreate, WaitlistEntryOut

router = APIRouter(tags=["waitlist"])


@router.post("/waitlist", response_model=WaitlistEntryOut, status_code=201)
def create_waitlist_entry(
    body: WaitlistCreate,
    session: DbSession,
    settings: AppSettings,
) -> WaitlistEntryOut:
    """Public. Persist a waitlist row. Does not require login."""
    if not settings.pc_waitlist:
        raise HTTPException(
            status_code=404,
            detail={"code": "waitlist_disabled", "message": "Waitlist is not enabled."},
        )

    entry = WaitlistEntry(
        name=body.name,
        email=str(body.email),
        phone=body.phone,
        notes=body.notes,
    )
    session.add(entry)
    try:
        session.flush()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail={
                "code": "duplicate_email",
                "message": "That email is already on the waitlist.",
            },
        ) from None
    session.refresh(entry)
    return WaitlistEntryOut.model_validate(entry)


@router.get("/waitlist", response_model=list[WaitlistEntryOut])
def list_waitlist_entries(
    session: DbSession,
    _owner: Owner,
    settings: AppSettings,
) -> list[WaitlistEntryOut]:
    """Owner list. Newest first."""
    if not settings.pc_waitlist:
        raise HTTPException(
            status_code=404,
            detail={"code": "waitlist_disabled", "message": "Waitlist is not enabled."},
        )

    rows = session.scalars(
        select(WaitlistEntry).order_by(WaitlistEntry.created_at.desc())
    ).all()
    return [WaitlistEntryOut.model_validate(row) for row in rows]
