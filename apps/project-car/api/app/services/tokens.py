"""Append-only token ledger.

apply_ledger is the writer that inserts a token_transactions row and moves the
allowance and purchased piles. After every write, token_balance equals
allowance_balance plus purchased_balance, including when those three numbers
were already apart. rebuild_token_balance sets the piles from their column
sums and sets token_balance to that sum. It inserts no row.
grant_period_allocations calls apply_ledger for each active member who does
not already have this America/Regina month's monthly_allocation. A row tagged
with tz America/Regina and a period counts only for that period. A row with
no such tag counts when created_at falls in the month. The owner request is
the only caller.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.models import Member, MemberStatus, TokenTransaction, TokenTransactionKind
from app.shop_time import PRICING_TZ, pricing_now

PERIOD_TZ = "America/Regina"
_PURCHASE_KIND = "token_purchase"


def _kind_value(kind: TokenTransactionKind) -> str:
    if isinstance(kind, TokenTransactionKind):
        return kind.value
    return str(kind)


def _default_piles(member: Member, kind: TokenTransactionKind, amount: Decimal) -> tuple[Decimal, Decimal]:
    """Split a ledger amount when the caller does not name the piles.

    A purchase credits the purchased pile. Any other credit, including a
    grant, a refund, and a positive adjustment, credits allowance. A spend
    takes allowance first, then purchased.
    """
    if _kind_value(kind) == _PURCHASE_KIND:
        return Decimal("0"), amount
    if amount >= 0:
        return amount, Decimal("0")
    take = -amount
    allowance = Decimal(member.allowance_balance)
    from_allowance = min(allowance, take) if allowance > 0 else Decimal("0")
    return -from_allowance, -(take - from_allowance)


def _conflict(code: str, message: str) -> HTTPException:
    return HTTPException(status_code=409, detail={"code": code, "message": message})


def _conflict_code(exc: IntegrityError) -> str:
    orig = getattr(exc, "orig", None)
    diag = getattr(orig, "diag", None)
    constraint = getattr(diag, "constraint_name", None) or ""
    message = " ".join(part for part in (str(constraint), str(orig) if orig is not None else str(exc)) if part)
    if "payment_ref" in message or "uq_token_transactions_payment_ref" in message:
        return "already_credited"
    return "duplicate_ledger_entry"


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
            status_code=400,
            detail={
                "code": "pile_mismatch",
                "message": "The allowance and purchased amounts must sum to the ledger amount.",
            },
        )
    # Trust the piles. A cache that had drifted is pulled back onto the sum.
    new_allowance = Decimal(member.allowance_balance) + allowance_amount
    new_purchased = Decimal(member.purchased_balance) + purchased_amount
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
    member.token_balance = new_allowance + new_purchased
    session.add(member)
    try:
        session.flush()
    except IntegrityError as exc:
        # One reserve, refund, and debit per booking, and one credit per
        # payment id. The rollback also undoes the pile move above.
        session.rollback()
        if _conflict_code(exc) == "already_credited":
            raise _conflict("already_credited", "That payment has already been credited.") from None
        raise _conflict(
            "duplicate_ledger_entry",
            f"This booking already has a {_kind_value(kind)} ledger row.",
        ) from None
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
    member.allowance_balance = _pile_sum(session, member.id, TokenTransaction.allowance_amount)
    member.purchased_balance = _pile_sum(session, member.id, TokenTransaction.purchased_amount)
    member.token_balance = member.allowance_balance + member.purchased_balance
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
    """Grant each active member included_tokens once for this Regina month.

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
        amount = Decimal(member.tier.included_tokens)
        apply_ledger(
            session,
            member,
            kind=TokenTransactionKind.MONTHLY_ALLOCATION,
            amount=amount,
            note=f"{period} {member.tier.display_name} allocation",
            meta={"period": period, "tz": PERIOD_TZ},
        )
        granted.append(PeriodGrant(member_id=member.id, tier_name=member.tier_name, amount=amount))
    return PeriodAllocationResult(period=period, tz=PERIOD_TZ, granted=granted, skipped=skipped)
