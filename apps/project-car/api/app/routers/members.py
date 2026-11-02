from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from app.auth import hash_password
from app.deps import DbSession, Owner
from app.models import (
    BillingTransaction,
    Booking,
    Member,
    MembershipTier,
    TokenTransaction,
    TokenTransactionKind,
)
from app.schemas import (
    BookingOut,
    DepositCreate,
    DollarChargeOut,
    MemberCreate,
    MemberDetailOut,
    MemberOut,
    MemberPasswordSet,
    MemberPatch,
    TokenAdjustment,
    TokenPurchaseCreate,
    TokenTransactionOut,
)
from app.services.bookings import lock_member
from app.services.staff import reject_ai
from app.services.tokens import apply_ledger, rebuild_token_balance, record_deposit, record_token_purchase

router = APIRouter(tags=["members"])

# Stand-in until Ben sets the real minimum. A spaces-only value still fails at this length.
MEMBER_PASSWORD_MIN_LENGTH = 12

# Stand-in until Ben sets the real cap. Absolute value at or above this is refused.
MAX_TOKEN_ADJUSTMENT = Decimal("1000000")
# D11 default until Ben decides: every Owner balance override says why.
OVERRIDE_REASON_MIN = 3
OVERRIDE_REASON_MAX = 500


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
    # name and status are NOT NULL. An explicit null flushes as IntegrityError (500).
    # tier_name null stays the 400 unknown_tier path above.
    null_required = [key for key in ("name", "status") if key in updates and updates[key] is None]
    if null_required:
        if null_required == ["name", "status"]:
            message = "Name and status cannot be null."
        elif null_required == ["name"]:
            message = "Name cannot be null."
        else:
            message = "Status cannot be null."
        raise HTTPException(
            status_code=422,
            detail={"code": "validation_error", "message": message},
        )
    if "name" in updates and updates["name"]:
        updates["name"] = updates["name"].strip()
    for key, value in updates.items():
        setattr(member, key, value)
    session.add(member)
    session.flush()
    session.refresh(member)
    return MemberOut.model_validate(member)


@router.post("/members/{member_id}/password", response_model=MemberOut)
def set_member_password(
    member_id: UUID,
    body: dict,
    session: DbSession,
    _owner: Owner,
) -> MemberOut:
    """Store a new scrypt hash. The plaintext is not stored, logged, or returned."""
    try:
        password = MemberPasswordSet.model_validate(body).password
    except ValidationError:
        raise HTTPException(
            status_code=422,
            detail={"code": "validation_error", "message": "Password is required."},
        ) from None
    # Length is the raw string. Spaces-only is rejected even when it meets the count.
    if len(password) < MEMBER_PASSWORD_MIN_LENGTH or password.isspace():
        raise HTTPException(
            status_code=422,
            detail={
                "code": "password_too_short",
                "message": (
                    f"Password must be at least {MEMBER_PASSWORD_MIN_LENGTH} characters"
                    " and cannot be only spaces."
                ),
            },
        )
    member = _member_or_404(session, member_id)
    member.password_hash = hash_password(password)
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
    owner: Owner,
) -> TokenTransactionOut:
    reject_ai(
        owner,
        code="token_change_requires_human",
        message="An AI cannot change a token balance on its own.",
    )
    reason = (body.reason or "").strip()
    if not OVERRIDE_REASON_MIN <= len(reason) <= OVERRIDE_REASON_MAX:
        raise HTTPException(
            status_code=422,
            detail={
                "code": "reason_required",
                "message": (
                    f"An adjustment needs a reason of {OVERRIDE_REASON_MIN}-"
                    f"{OVERRIDE_REASON_MAX} characters."
                ),
            },
        )
    # Lock before apply_ledger reads token_balance. Two adjustments otherwise
    # both add to the same cached balance and the second write drops the first.
    member = lock_member(session, member_id)
    amount = body.amount
    # Refuse the posted scale. Rounding to cents would store 0.00 for 0.0001.
    exponent = amount.as_tuple().exponent
    if not isinstance(exponent, int) or exponent < -2:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "invalid_tokens",
                "message": "Adjustment amount must have at most 2 decimal places.",
            },
        )
    if abs(amount) >= MAX_TOKEN_ADJUSTMENT:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "invalid_tokens",
                "message": "Adjustment amount must be under 1,000,000 tokens.",
            },
        )
    if amount == 0:
        raise HTTPException(
            status_code=400,
            detail={"code": "invalid_tokens", "message": "Adjustment amount cannot be zero."},
        )
    row = apply_ledger(
        session,
        member,
        kind=TokenTransactionKind.ADMIN_ADJUSTMENT,
        amount=amount,
        note=body.note or reason,
        meta={"override": {"reason": reason, "by": owner.email}},
    )
    session.flush()
    session.refresh(row)
    return TokenTransactionOut.model_validate(row)


@router.post(
    "/members/{member_id}/token-purchases",
    response_model=TokenTransactionOut,
    status_code=201,
)
def record_member_token_purchase(
    member_id: UUID,
    body: TokenPurchaseCreate,
    session: DbSession,
    owner: Owner,
) -> TokenTransactionOut:
    """Credit tokens for one PayPal payment. The payment id credits once."""
    reject_ai(
        owner,
        code="token_change_requires_human",
        message="An AI cannot change a token balance on its own.",
    )
    if body.tokens >= MAX_TOKEN_ADJUSTMENT:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "invalid_tokens",
                "message": "A purchase must be under 1,000,000 tokens.",
            },
        )
    member = lock_member(session, member_id)
    row = record_token_purchase(
        session,
        member,
        payment_id=body.payment_id,
        tokens=body.tokens,
        subtotal_cad=body.subtotal_cad,
        recorded_by=owner.email,
        note=body.note,
    )
    session.refresh(row)
    return TokenTransactionOut.model_validate(row)


@router.get("/members/{member_id}/dollar-charges", response_model=list[DollarChargeOut])
def list_dollar_charges(member_id: UUID, session: DbSession, _owner: Owner) -> list[DollarChargeOut]:
    _member_or_404(session, member_id)
    rows = session.scalars(
        select(BillingTransaction)
        .where(
            BillingTransaction.member_id == member_id,
            BillingTransaction.subtotal_cad.is_not(None),
        )
        .order_by(BillingTransaction.created_at, BillingTransaction.id)
    ).all()
    return [
        DollarChargeOut(
            id=row.id,
            purpose=row.kind.value,
            payment_id=row.payment_id,
            subtotal_cad=Decimal(row.subtotal_cad or 0),
            gst_cad=Decimal(row.gst_cad or 0),
            total_cad=Decimal(row.total_cad or 0),
            gst_rate=Decimal(row.gst_rate or 0),
            created_at=row.created_at,
        )
        for row in rows
    ]


@router.post("/members/{member_id}/deposits", response_model=DollarChargeOut, status_code=201)
def post_deposit(
    member_id: UUID,
    body: DepositCreate,
    session: DbSession,
    owner: Owner,
) -> DollarChargeOut:
    """Take, return, or keep a damage deposit. Stand-in payment id. No tokens."""
    reject_ai(
        owner,
        code="deposit_requires_human",
        message="An AI cannot move a deposit on its own.",
    )
    member = lock_member(session, member_id)
    row = record_deposit(
        session,
        member,
        action=body.action,
        amount=body.amount,
        payment_id=body.payment_id,
        note=body.note,
    )
    return DollarChargeOut(
        id=row.id,
        purpose=row.kind.value,
        payment_id=row.payment_id,
        subtotal_cad=Decimal(row.subtotal_cad or 0),
        gst_cad=Decimal(row.gst_cad or 0),
        total_cad=Decimal(row.total_cad or 0),
        gst_rate=Decimal(row.gst_rate or 0),
        created_at=row.created_at,
    )


@router.post("/members/{member_id}/tokens/rebuild", response_model=MemberOut)
def rebuild_member_tokens(member_id: UUID, session: DbSession, _owner: Owner) -> MemberOut:
    """Set the cached balance from the ledger sum. Inserts no ledger row."""
    member = _member_or_404(session, member_id)
    rebuild_token_balance(session, member)
    session.flush()
    session.refresh(member)
    return MemberOut.model_validate(member)
