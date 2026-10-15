from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.deps import AppSettings, DbSession, Owner
from app.models import Member, MemberStatus, MembershipTier, TokenTransactionKind, WaitlistEntry
from app.schemas import WaitlistCreate, WaitlistEntryOut
from app.services.tokens import apply_ledger

router = APIRouter(tags=["waitlist"])


class WaitlistConvert(BaseModel):
    tier_name: str = Field(min_length=1, max_length=64)

    @field_validator("tier_name")
    @classmethod
    def normalize_tier(cls, value: str) -> str:
        cleaned = value.strip().lower()
        if not cleaned:
            raise ValueError("Tier is required.")
        return cleaned


@router.post("/waitlist", response_model=WaitlistEntryOut, status_code=201)
def create_waitlist_entry(
    body: WaitlistCreate,
    session: DbSession,
    settings: AppSettings,
) -> WaitlistEntryOut:
    """Public. Persist a waitlist row. No Owner cookie or bearer token."""
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


@router.post("/waitlist/{entry_id}/contacted", response_model=WaitlistEntryOut)
def mark_waitlist_contacted(entry_id: UUID, session: DbSession, _owner: Owner) -> WaitlistEntryOut:
    entry = session.get(WaitlistEntry, entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail={"code": "not_found", "message": "Waitlist entry not found."})
    if entry.contacted_at is None:
        entry.contacted_at = datetime.now(timezone.utc)
        session.add(entry)
        session.flush()
        session.refresh(entry)
    return WaitlistEntryOut.model_validate(entry)


@router.post("/waitlist/{entry_id}/convert", response_model=WaitlistEntryOut)
def convert_waitlist_entry(
    entry_id: UUID,
    body: WaitlistConvert,
    session: DbSession,
    _owner: Owner,
) -> WaitlistEntryOut:
    """Owner. One waitlist row becomes one active member and one initial grant."""
    entry = session.get(WaitlistEntry, entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail={"code": "not_found", "message": "Waitlist entry not found."})
    if entry.member_id is not None:
        raise HTTPException(
            status_code=409,
            detail={"code": "already_converted", "message": "That waitlist row is already a member."},
        )

    tier = session.get(MembershipTier, body.tier_name)
    if tier is None:
        raise HTTPException(status_code=400, detail={"code": "unknown_tier", "message": "Unknown membership tier."})

    existing = session.scalar(select(Member).where(Member.email == entry.email))
    if existing is not None:
        raise HTTPException(
            status_code=409,
            detail={"code": "duplicate_email", "message": "A member with that email already exists."},
        )

    member = Member(
        name=entry.name,
        email=entry.email,
        phone=entry.phone,
        tier_name=tier.name,
        status=MemberStatus.ACTIVE,
        token_balance=Decimal("0"),
        deposit_balance=Decimal("0"),
    )
    session.add(member)
    try:
        session.flush()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail={"code": "duplicate_email", "message": "A member with that email already exists."},
        ) from None

    if tier.included_tokens:
        apply_ledger(
            session,
            member,
            kind=TokenTransactionKind.MONTHLY_ALLOCATION,
            amount=Decimal(tier.included_tokens),
            note=f"Initial {tier.display_name} allocation",
        )

    entry.member_id = member.id
    session.add(entry)
    session.flush()
    session.refresh(entry)
    return WaitlistEntryOut.model_validate(entry)
