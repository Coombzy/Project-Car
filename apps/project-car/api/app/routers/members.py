from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from app.deps import DbSession, Owner
from app.models import Booking, Member, MembershipTier, TokenTransaction, TokenTransactionKind
from app.schemas import (
    BookingOut,
    MemberCreate,
    MemberDetailOut,
    MemberOut,
    MemberPatch,
    TokenAdjustment,
    TokenTransactionOut,
)
from app.services.tokens import apply_ledger

router = APIRouter(tags=["members"])


def _member_or_404(session, member_id: UUID) -> Member:
    member = session.get(Member, member_id)
    if member is None:
        raise HTTPException(status_code=404, detail={"code": "not_found", "message": "Member not found."})
    return member


@router.get("/members", response_model=list[MemberOut])
def list_members(session: DbSession, _owner: Owner) -> list[MemberOut]:
    rows = session.scalars(select(Member).order_by(Member.name)).all()
    return [MemberOut.model_validate(row) for row in rows]


@router.post("/members", response_model=MemberOut, status_code=201)
def create_member(body: MemberCreate, session: DbSession, _owner: Owner) -> MemberOut:
    tier = session.get(MembershipTier, body.tier_name)
    if tier is None:
        raise HTTPException(status_code=400, detail={"code": "unknown_tier", "message": "Unknown membership tier."})

    member = Member(
        name=body.name,
        email=str(body.email),
        phone=body.phone,
        tier_name=tier.name,
        status=body.status,
        waiver_signed_at=body.waiver_signed_at,
        waiver_version=body.waiver_version,
        emergency_contact_name=body.emergency_contact_name,
        emergency_contact_phone=body.emergency_contact_phone,
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

    if body.allocate_tokens and tier.included_tokens:
        apply_ledger(
            session,
            member,
            kind=TokenTransactionKind.MONTHLY_ALLOCATION,
            amount=Decimal(tier.included_tokens),
            note=f"Initial {tier.display_name} allocation",
        )
    session.refresh(member)
    return MemberOut.model_validate(member)


@router.get("/members/{member_id}", response_model=MemberDetailOut)
def get_member(member_id: UUID, session: DbSession, _owner: Owner) -> MemberDetailOut:
    member = session.scalars(
        select(Member)
        .options(
            selectinload(Member.bookings).selectinload(Booking.hoist),
            selectinload(Member.bookings).selectinload(Booking.member),
        )
        .where(Member.id == member_id)
    ).first()
    if member is None:
        raise HTTPException(status_code=404, detail={"code": "not_found", "message": "Member not found."})

    base = MemberOut.model_validate(member)
    return MemberDetailOut(
        **base.model_dump(),
        bookings=[
            BookingOut.from_booking(row)
            for row in sorted(member.bookings, key=lambda booking: booking.start_at, reverse=True)
        ],
    )


@router.patch("/members/{member_id}", response_model=MemberOut)
def patch_member(member_id: UUID, body: MemberPatch, session: DbSession, _owner: Owner) -> MemberOut:
    member = _member_or_404(session, member_id)
    updates = body.model_dump(exclude_unset=True)
    if "tier_name" in updates:
        updates["tier_name"] = str(updates["tier_name"]).strip().lower()
        if session.get(MembershipTier, updates["tier_name"]) is None:
            raise HTTPException(status_code=400, detail={"code": "unknown_tier", "message": "Unknown membership tier."})
    if "name" in updates and updates["name"]:
        updates["name"] = updates["name"].strip()
    for key, value in updates.items():
        setattr(member, key, value)
    session.add(member)
    session.flush()
    session.refresh(member)
    return MemberOut.model_validate(member)


@router.get("/members/{member_id}/tokens", response_model=list[TokenTransactionOut])
def list_member_tokens(member_id: UUID, session: DbSession, _owner: Owner) -> list[TokenTransactionOut]:
    _member_or_404(session, member_id)
    rows = session.scalars(
        select(TokenTransaction)
        .where(TokenTransaction.member_id == member_id)
        .order_by(TokenTransaction.created_at.desc())
    ).all()
    return [TokenTransactionOut.model_validate(row) for row in rows]


@router.post("/members/{member_id}/tokens", response_model=TokenTransactionOut, status_code=201)
def adjust_member_tokens(
    member_id: UUID,
    body: TokenAdjustment,
    session: DbSession,
    _owner: Owner,
) -> TokenTransactionOut:
    member = _member_or_404(session, member_id)
    if body.amount == 0:
        raise HTTPException(
            status_code=400,
            detail={"code": "invalid_tokens", "message": "Adjustment amount cannot be zero."},
        )
    row = apply_ledger(
        session,
        member,
        kind=TokenTransactionKind.ADMIN_ADJUSTMENT,
        amount=body.amount,
        note=body.note or "Owner adjustment",
    )
    session.flush()
    session.refresh(row)
    return TokenTransactionOut.model_validate(row)
