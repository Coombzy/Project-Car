"""Append-only token ledger. Never change member.token_balance without a row."""

from __future__ import annotations

from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Member, TokenTransaction, TokenTransactionKind


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
