"""Append-only token ledger.

apply_ledger is the writer that inserts a token_transactions row and moves the
cache by that amount. rebuild_token_balance only sets the cache from the ledger
sum and inserts no row. grant_period_allocations calls apply_ledger for each
active member who does not already have this America/Regina month's
monthly_allocation. A row tagged with tz America/Regina and a period counts
only for that period. A row with no such tag counts when created_at falls in
the month. The owner request is the only caller.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import ROUND_HALF_UP, Decimal
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.models import (
    BillingKind,
    BillingTransaction,
    Member,
    MemberStatus,
    TokenTransaction,
    TokenTransactionKind,
)
from app.shop_time import PRICING_TZ, pricing_now

PERIOD_TZ = "America/Regina"
# Ben, D15: GST applies to every money transaction. Stand-in rate until his
# accountant confirms it.
GST_RATE = Decimal("0.05")
CENTS = Decimal("0.01")
# Ben, D10: no balance goes below zero, ever. There is no Owner allow path.
TOKEN_BALANCE_FLOOR = Decimal("0")


def piles_for_refund(
    allowance_spent: Decimal,
    purchased_spent: Decimal,
    refund: Decimal,
) -> tuple[Decimal, Decimal]:
    """Restore a cancel onto the piles it came from, purchased first.

    Spent figures are positive. The returned pair is the positive refund split
    and sums to ``refund``.
    """
    purchased_back = min(Decimal(purchased_spent), Decimal(refund))
    allowance_back = Decimal(refund) - purchased_back
    return allowance_back, purchased_back


def _default_piles(member: Member, kind: TokenTransactionKind, amount: Decimal) -> tuple[Decimal, Decimal]:
    """Split a ledger amount when the caller does not name the piles.

    Purchases credit the purchased pile. Grants, expiry, and positive
    adjustments credit allowance. A spend takes allowance first, then purchased.
    """
    if kind == TokenTransactionKind.TOKEN_PURCHASE:
        return Decimal("0"), amount
    if kind in (TokenTransactionKind.MONTHLY_ALLOCATION, TokenTransactionKind.ALLOWANCE_EXPIRY):
        return amount, Decimal("0")
    if amount > 0:
        return amount, Decimal("0")
    take = -amount
    from_allowance = min(Decimal(member.allowance_balance), take)
    return -from_allowance, -(take - from_allowance)


def apply_ledger(
    session: Session,
    member: Member,
    *,
    kind: TokenTransactionKind,
    amount: Decimal,
    booking_id=None,
    note: str | None = None,
    meta: dict | None = None,
    payment_ref: str | None = None,
    allowance_amount: Decimal | None = None,
    purchased_amount: Decimal | None = None,
) -> TokenTransaction:
    amount = Decimal(amount)
    if allowance_amount is None and purchased_amount is None:
        allowance_amount, purchased_amount = _default_piles(member, kind, amount)
    else:
        allowance_amount = Decimal("0") if allowance_amount is None else Decimal(allowance_amount)
        purchased_amount = Decimal("0") if purchased_amount is None else Decimal(purchased_amount)
    if allowance_amount + purchased_amount != amount:
        raise HTTPException(
            status_code=500,
            detail={
                "code": "pile_mismatch",
                "message": "The allowance and purchased amounts must sum to the ledger amount.",
            },
        )
    balance = Decimal(member.token_balance)
    new_allowance = Decimal(member.allowance_balance) + allowance_amount
    new_purchased = Decimal(member.purchased_balance) + purchased_amount
    new_balance = balance + amount
    if new_balance < TOKEN_BALANCE_FLOOR or new_allowance < TOKEN_BALANCE_FLOOR or new_purchased < TOKEN_BALANCE_FLOOR:
        raise HTTPException(
            status_code=409,
            detail={
                "code": "would_go_negative",
                "message": "That would take the balance below zero.",
                "balance": str(balance),
                "amount": str(amount),
            },
        )
    row = TokenTransaction(
        member_id=member.id,
        booking_id=booking_id,
        kind=kind,
        amount=amount,
        allowance_amount=allowance_amount,
        purchased_amount=purchased_amount,
        note=note,
        meta=meta,
        payment_ref=payment_ref,
    )
    session.add(row)
    member.allowance_balance = new_allowance
    member.purchased_balance = new_purchased
    member.token_balance = new_balance
    session.add(member)
    try:
        session.flush()
    except IntegrityError:
        # The unique indexes are the last guard: one reserve, refund and debit
        # per booking, and one credit per payment id. The rollback also undoes
        # the cache move above.
        session.rollback()
        if payment_ref is not None:
            raise _conflict("already_credited", "That payment has already been credited.") from None
        raise _conflict(
            "duplicate_ledger_entry",
            f"This booking already has a {kind.value} ledger row.",
        ) from None
    return row


def _conflict(code: str, message: str) -> HTTPException:
    return HTTPException(status_code=409, detail={"code": code, "message": message})


def _cents(value: Decimal) -> Decimal:
    return Decimal(value).quantize(CENTS, rounding=ROUND_HALF_UP)


def record_token_purchase(
    session: Session,
    member: Member,
    *,
    payment_id: str,
    tokens: Decimal,
    subtotal_cad: Decimal,
    recorded_by: str,
    note: str | None = None,
    processor: str | None = None,
) -> TokenTransaction:
    """Credit paid tokens once per payment id, with GST on the CAD subtotal."""
    already = session.scalar(
        select(TokenTransaction.id).where(TokenTransaction.payment_ref == payment_id)
    )
    if already is not None:
        raise _conflict("already_credited", "That payment has already been credited.")
    subtotal = _cents(subtotal_cad)
    gst = _cents(subtotal * GST_RATE)
    total = subtotal + gst
    purchase = {
        "payment_id": payment_id,
        "subtotal_cad": str(subtotal),
        "gst_rate": str(GST_RATE),
        "gst_cad": str(gst),
        "total_cad": str(total),
        "by": recorded_by,
    }
    if processor:
        purchase["processor"] = processor
    session.add(
        BillingTransaction(
            member_id=member.id,
            kind=BillingKind.PACK,
            amount=total,
            subtotal_cad=subtotal,
            gst_cad=gst,
            total_cad=total,
            gst_rate=GST_RATE,
            payment_id=payment_id,
            note=note or f"Token purchase {payment_id}",
        )
    )
    session.flush()
    return apply_ledger(
        session,
        member,
        kind=TokenTransactionKind.TOKEN_PURCHASE,
        amount=Decimal(tokens),
        note=note or f"Token purchase {payment_id}",
        meta={"purchase": purchase},
        payment_ref=payment_id,
    )


def record_deposit(
    session: Session,
    member: Member,
    *,
    action: str,
    amount: Decimal,
    payment_id: str,
    note: str | None = None,
) -> BillingTransaction:
    """Move a damage deposit. Take and return charge no GST and no tokens.

    Keep writes GST at the stand-in rate. The held dollars are the before-tax
    amount. Payment ids are stand-ins until a processor is connected.
    """
    held_amount = _cents(amount)
    if held_amount <= 0:
        raise HTTPException(
            status_code=400,
            detail={"code": "invalid_amount", "message": "Deposit amount must be greater than zero."},
        )
    payment_id = payment_id.strip()
    held = Decimal(member.deposit_balance)
    if action == "take":
        kind = BillingKind.DEPOSIT_TAKEN
        charge_gst = False
        member.deposit_balance = held + held_amount
    elif action == "return":
        if held_amount > held:
            raise HTTPException(
                status_code=400,
                detail={"code": "deposit_short", "message": "That is more than the deposit on file."},
            )
        kind = BillingKind.DEPOSIT_RETURNED
        charge_gst = False
        member.deposit_balance = held - held_amount
    elif action == "keep":
        if held_amount > held:
            raise HTTPException(
                status_code=400,
                detail={"code": "deposit_short", "message": "That is more than the deposit on file."},
            )
        kind = BillingKind.DEPOSIT_KEPT
        charge_gst = True
        member.deposit_balance = held - held_amount
    else:
        raise HTTPException(
            status_code=422,
            detail={"code": "validation_error", "message": "Deposit action must be take, return, or keep."},
        )
    gst = _cents(held_amount * GST_RATE) if charge_gst else Decimal("0.00")
    total = held_amount + gst
    row = BillingTransaction(
        member_id=member.id,
        kind=kind,
        amount=total,
        subtotal_cad=held_amount,
        gst_cad=gst,
        total_cad=total,
        gst_rate=GST_RATE if charge_gst else Decimal("0.0000"),
        payment_id=payment_id,
        note=note or f"Deposit {action} {payment_id}",
    )
    session.add(row)
    session.add(member)
    try:
        session.flush()
    except IntegrityError:
        session.rollback()
        raise _conflict("already_recorded", "That payment id is already on a dollar row.") from None
    session.refresh(row)
    return row


def ledger_sum(session: Session, member_id) -> Decimal:
    total = session.scalar(
        select(func.coalesce(func.sum(TokenTransaction.amount), 0)).where(
            TokenTransaction.member_id == member_id
        )
    )
    return Decimal(total)


def _pile_sum(session: Session, member_id, column) -> Decimal:
    total = session.scalar(
        select(func.coalesce(func.sum(column), 0)).where(TokenTransaction.member_id == member_id)
    )
    return Decimal(total)


def rebuild_token_balance(session: Session, member: Member) -> Decimal:
    member.token_balance = ledger_sum(session, member.id)
    member.allowance_balance = _pile_sum(session, member.id, TokenTransaction.allowance_amount)
    member.purchased_balance = _pile_sum(session, member.id, TokenTransaction.purchased_amount)
    session.add(member)
    return member.token_balance


@dataclass(frozen=True)
class PeriodGrant:
    member_id: UUID
    tier_name: str
    amount: Decimal


@dataclass(frozen=True)
class PeriodAllocationResult:
    period: str
    tz: str
    granted: list[PeriodGrant]
    skipped: int


def _ledger_instant(value: datetime) -> datetime:
    """Ledger created_at is func.now(), which is UTC.

    SQLite returns that UTC clock with tzinfo stripped. Postgres returns an
    aware instant. as_utc() would read the naive UTC clock as America/Edmonton
    and can move a row across the Regina month boundary.
    """
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def regina_period(now: datetime | None = None) -> tuple[datetime, datetime, str]:
    """Half-open Regina calendar month containing `now`, plus `YYYY-MM`."""
    local = (now or pricing_now()).astimezone(PRICING_TZ)
    start = datetime(local.year, local.month, 1, tzinfo=PRICING_TZ)
    if local.month == 12:
        end = datetime(local.year + 1, 1, 1, tzinfo=PRICING_TZ)
    else:
        end = datetime(local.year, local.month + 1, 1, tzinfo=PRICING_TZ)
    return start, end, f"{local.year:04d}-{local.month:02d}"


def _in_period(created_at: datetime, start: datetime, end: datetime) -> bool:
    instant = _ledger_instant(created_at)
    return start.astimezone(timezone.utc) <= instant < end.astimezone(timezone.utc)


def _tagged_period(meta: dict | None, period: str) -> bool:
    if not isinstance(meta, dict):
        return False
    return meta.get("period") == period and meta.get("tz") == PERIOD_TZ


def _has_regina_period_tag(meta: dict | None) -> bool:
    return isinstance(meta, dict) and meta.get("tz") == PERIOD_TZ and "period" in meta


def _has_period_allocation(
    rows: list[TokenTransaction],
    start: datetime,
    end: datetime,
    period: str,
) -> bool:
    """A tagged Regina period counts only for that period.

    created_at counts only when meta has no America/Regina period tag.
    That is the initial member-create grant. A row tagged for month N
    whose created_at falls in month N+1 must not consume N+1.
    """
    for row in rows:
        if _has_regina_period_tag(row.meta):
            if _tagged_period(row.meta, period):
                return True
            continue
        if _in_period(row.created_at, start, end):
            return True
    return False


def grant_period_allocations(session: Session, now: datetime | None = None) -> PeriodAllocationResult:
    """Expire unused allowance above one month, then grant this Regina month.

    Purchased tokens are a separate pile and are not expired. A booking spends
    allowance first, so tokens already reserved are not in allowance_balance.

    A row tagged tz=America/Regina with a period counts only for that period.
    A row with no such tag counts when created_at is in this month, including
    the initial grant from member create. A second call inserts nothing.
    No scheduler.

    Active members are locked in name, id order before that ledger read.
    On Postgres the second grant waits for the first commit, then sees its
    monthly_allocation rows. SQLite drops FOR UPDATE.
    """
    start, end, period = regina_period(now)
    members = list(
        session.scalars(
            select(Member)
            .where(Member.status == MemberStatus.ACTIVE)
            .options(selectinload(Member.tier))
            .order_by(Member.name, Member.id)
            .with_for_update()
        ).all()
    )
    by_member: dict[UUID, list[TokenTransaction]] = {}
    if members:
        existing = session.scalars(
            select(TokenTransaction).where(
                TokenTransaction.member_id.in_([member.id for member in members]),
                TokenTransaction.kind == TokenTransactionKind.MONTHLY_ALLOCATION,
            )
        ).all()
        for row in existing:
            by_member.setdefault(row.member_id, []).append(row)

    granted: list[PeriodGrant] = []
    skipped = 0
    for member in members:
        if _has_period_allocation(by_member.get(member.id, []), start, end, period):
            skipped += 1
            continue
        if member.tier.included_tokens <= 0:
            continue
        allowance = Decimal(member.tier.included_tokens)
        # Upcoming visits are already taken off allowance_balance. A cancel
        # after this grant can put allowance above two months until the next
        # grant. Purchased tokens are not part of this cap.
        expire = Decimal(member.allowance_balance) - allowance
        if expire > 0:
            apply_ledger(
                session,
                member,
                kind=TokenTransactionKind.ALLOWANCE_EXPIRY,
                amount=-expire,
                note=f"{period} allowance expiry",
                meta={"period": period, "tz": PERIOD_TZ},
            )
        apply_ledger(
            session,
            member,
            kind=TokenTransactionKind.MONTHLY_ALLOCATION,
            amount=allowance,
            note=(
                f"{period} {member.tier.display_name} allocation. "
                "A cancel after this grant can put the balance above two months until the next grant."
            ),
            meta={"period": period, "tz": PERIOD_TZ},
        )
        granted.append(PeriodGrant(member_id=member.id, tier_name=member.tier_name, amount=allowance))
    return PeriodAllocationResult(period=period, tz=PERIOD_TZ, granted=granted, skipped=skipped)
