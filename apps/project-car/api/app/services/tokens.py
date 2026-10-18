"""Append-only token ledger.

apply_ledger is the writer that inserts a token_transactions row and moves the
cache by that amount. rebuild_token_balance only sets the cache from the ledger
sum and inserts no row. grant_period_allocations calls apply_ledger for each
active member who does not already have a monthly_allocation in the current
America/Regina calendar month. The owner request is the only caller.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models import Member, MemberStatus, TokenTransaction, TokenTransactionKind
from app.shop_time import PRICING_TZ, pricing_now

PERIOD_TZ = "America/Regina"


def apply_ledger(
    session: Session,
    member: Member,
    *,
    kind: TokenTransactionKind,
    amount: Decimal,
    booking_id=None,
    note: str | None = None,
    meta: dict | None = None,
) -> TokenTransaction:
    amount = Decimal(amount)
    row = TokenTransaction(
        member_id=member.id,
        booking_id=booking_id,
        kind=kind,
        amount=amount,
        note=note,
        meta=meta,
    )
    session.add(row)
    member.token_balance = Decimal(member.token_balance) + amount
    session.add(member)
    session.flush()
    return row


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


def _has_period_allocation(
    rows: list[TokenTransaction],
    start: datetime,
    end: datetime,
    period: str,
) -> bool:
    return any(_tagged_period(row.meta, period) or _in_period(row.created_at, start, end) for row in rows)


def grant_period_allocations(session: Session, now: datetime | None = None) -> PeriodAllocationResult:
    """Grant each active member included_tokens once for this Regina month.

    A monthly_allocation already in this month counts, including the initial
    grant from member create. A second call inserts nothing. No scheduler.
    """
    start, end, period = regina_period(now)
    members = list(
        session.scalars(
            select(Member)
            .where(Member.status == MemberStatus.ACTIVE)
            .options(selectinload(Member.tier))
            .order_by(Member.name, Member.id)
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
