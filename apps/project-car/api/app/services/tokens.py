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

from app.models import Member, MemberStatus, TokenTransaction, TokenTransactionKind
from app.shop_time import PRICING_TZ, pricing_now

PERIOD_TZ = "America/Regina"
# Ben, D15: GST applies to every money transaction. Stand-in rate until his
# accountant confirms it.
GST_RATE = Decimal("0.05")
CENTS = Decimal("0.01")
# Ben, D10: no balance goes below zero, ever. There is no Owner allow path.
TOKEN_BALANCE_FLOOR = Decimal("0")


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
) -> TokenTransaction:
    amount = Decimal(amount)
    balance = Decimal(member.token_balance)
    if amount < 0 and balance + amount < TOKEN_BALANCE_FLOOR:
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
        note=note,
        meta=meta,
        payment_ref=payment_ref,
    )
    session.add(row)
    member.token_balance = balance + amount
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
) -> TokenTransaction:
    """Credit paid tokens once per payment id, with GST on the CAD subtotal."""
    already = session.scalar(
        select(TokenTransaction.id).where(TokenTransaction.payment_ref == payment_id)
    )
    if already is not None:
        raise _conflict("already_credited", "That payment has already been credited.")
    subtotal = _cents(subtotal_cad)
    gst = _cents(subtotal * GST_RATE)
    purchase = {
        "payment_id": payment_id,
        "subtotal_cad": str(subtotal),
        "gst_rate": str(GST_RATE),
        "gst_cad": str(gst),
        "total_cad": str(subtotal + gst),
        "by": recorded_by,
    }
    return apply_ledger(
        session,
        member,
        kind=TokenTransactionKind.TOKEN_PURCHASE,
        amount=Decimal(tokens),
        note=note or f"Token purchase {payment_id}",
        meta={"purchase": purchase},
        payment_ref=payment_id,
    )


def ledger_sum(session: Session, member_id) -> Decimal:
    total = session.scalar(
        select(func.coalesce(func.sum(TokenTransaction.amount), 0)).where(
            TokenTransaction.member_id == member_id
        )
    )
    return Decimal(total)


def rebuild_token_balance(session: Session, member: Member) -> Decimal:
    member.token_balance = ledger_sum(session, member.id)
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
    """Expire spendable above one allowance, then grant this Regina month.

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
        # Spendable is the balance. Upcoming visits are already taken off it.
        # A cancel after this grant can put the balance above two months until
        # the next grant. Bought tokens are not a separate pile yet.
        expire = Decimal(member.token_balance) - allowance
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
