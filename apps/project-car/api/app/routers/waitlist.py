from __future__ import annotations

import threading
import time
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.client_ip import client_ip
from app.config import get_settings
from app.deps import AppSettings, DbSession, Owner
from app.models import Member, MemberStatus, MembershipTier, TokenTransactionKind, WaitlistEntry
from app.schemas import WaitlistCreate, WaitlistEntryOut
from app.services.tokens import apply_ledger

router = APIRouter(tags=["waitlist"])

# Eight creates inside this window lock the client IP.
# Same length as the login failure window in app.auth (15 minutes).
_WAITLIST_CREATE_LIMIT = 8
_WAITLIST_CREATE_WINDOW_SECONDS = 15 * 60


class _CreateStamp:
    """One reserved waitlist create. A failed insert drops this same object."""

    __slots__ = ("at",)

    def __init__(self, at: float) -> None:
        self.at = at


# Reserved creates keyed by client IP. One bucket per process.
_waitlist_creates: dict[str, list[_CreateStamp]] = {}
_waitlist_creates_lock = threading.Lock()


class WaitlistConvert(BaseModel):
    tier_name: str = Field(min_length=1, max_length=64)

    @field_validator("tier_name")
    @classmethod
    def normalize_tier(cls, value: str) -> str:
        cleaned = value.strip().lower()
        if not cleaned:
            raise ValueError("Tier is required.")
        return cleaned


def _client_ip(request: Request) -> str:
    return client_ip(request, get_settings().client_ip_header)


def _duplicate_email() -> HTTPException:
    return HTTPException(
        status_code=409,
        detail={
            "code": "duplicate_email",
            "message": "That email is already on the waitlist.",
        },
    )


def _rate_limited() -> HTTPException:
    return HTTPException(
        status_code=429,
        detail={
            "code": "rate_limited",
            "message": "Too many waitlist signups. Try again later.",
        },
    )


def _fresh_creates(client_ip: str, now: float) -> list[_CreateStamp]:
    """Caller holds `_waitlist_creates_lock`."""
    fresh = [
        stamp
        for stamp in _waitlist_creates.get(client_ip, ())
        if now - stamp.at <= _WAITLIST_CREATE_WINDOW_SECONDS
    ]
    if fresh:
        _waitlist_creates[client_ip] = fresh
    else:
        _waitlist_creates.pop(client_ip, None)
    return fresh


def _reserve_waitlist_create(client_ip: str) -> _CreateStamp | None:
    """Reserve one create slot before the insert.

    The cap check and the reservation share one lock, so two overlapping
    creates cannot both pass when this IP is one under the cap. The bucket
    is in-process. Each API process keeps its own counts. Returns the
    reserved stamp, or None when the IP is already at the cap.
    """
    now = time.monotonic()
    with _waitlist_creates_lock:
        stamps = _fresh_creates(client_ip, now)
        if len(stamps) >= _WAITLIST_CREATE_LIMIT:
            return None
        stamp = _CreateStamp(now)
        stamps.append(stamp)
        _waitlist_creates[client_ip] = stamps
        return stamp


def _release_waitlist_create(client_ip: str, stamp: _CreateStamp) -> None:
    """Drop a slot reserved for an insert that did not store a row."""
    with _waitlist_creates_lock:
        current = _waitlist_creates.get(client_ip)
        if not current:
            return
        kept = [item for item in current if item is not stamp]
        if len(kept) == len(current):
            return
        if kept:
            _waitlist_creates[client_ip] = kept
        else:
            _waitlist_creates.pop(client_ip, None)


@router.post("/waitlist", response_model=WaitlistEntryOut, status_code=201)
def create_waitlist_entry(
    body: WaitlistCreate,
    request: Request,
    session: DbSession,
    settings: AppSettings,
) -> WaitlistEntryOut:
    """Public. Persist a waitlist row. No Owner cookie or bearer token.

    Eight new emails from one client IP are stored per window. The next
    create is 429 and is not stored. An email already on the list is 409
    and does not take a slot.
    """
    if not settings.pc_waitlist:
        raise HTTPException(
            status_code=404,
            detail={"code": "waitlist_disabled", "message": "Waitlist is not enabled."},
        )

    email = str(body.email)
    existing = session.scalar(select(WaitlistEntry).where(WaitlistEntry.email == email))
    if existing is not None:
        raise _duplicate_email()

    client_ip = _client_ip(request)
    stamp = _reserve_waitlist_create(client_ip)
    if stamp is None:
        raise _rate_limited()

    entry = WaitlistEntry(
        name=body.name,
        email=email,
        phone=body.phone,
        notes=body.notes,
    )
    session.add(entry)
    try:
        session.flush()
    except IntegrityError:
        session.rollback()
        _release_waitlist_create(client_ip, stamp)
        raise _duplicate_email() from None
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
