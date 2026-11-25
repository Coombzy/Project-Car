"""Read-only check: cached member balances against ledger sums.

No writes, no commits, no alembic.
"""

from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Member, TokenTransaction

_ZERO = Decimal("0")


def _money(value: object) -> Decimal:
    if value is None:
        return _ZERO
    return value if isinstance(value, Decimal) else Decimal(str(value))


def _mismatches(session: Session) -> list[tuple]:
    summed = {
        member_id: (_money(allowance), _money(purchased))
        for member_id, allowance, purchased in session.execute(
            select(
                TokenTransaction.member_id,
                func.coalesce(func.sum(TokenTransaction.allowance_amount), 0),
                func.coalesce(func.sum(TokenTransaction.purchased_amount), 0),
            ).group_by(TokenTransaction.member_id)
        ).all()
    }
    found: list[tuple] = []
    for member in session.scalars(select(Member)).all():
        allowance_sum, purchased_sum = summed.get(member.id, (_ZERO, _ZERO))
        allowance, purchased = _money(member.allowance_balance), _money(member.purchased_balance)
        token = _money(member.token_balance)
        if token == allowance + purchased and allowance == allowance_sum and purchased == purchased_sum:
            continue
        found.append((str(member.id), token, allowance, purchased, allowance_sum, purchased_sum))
    found.sort(key=lambda row: row[0])
    return found


def mismatched_members(session: Session) -> list[str]:
    return [row[0] for row in _mismatches(session)]


def main(session: Session | None = None) -> int:
    owns = session is None
    if session is None:
        session = SessionLocal()
    try:
        rows = _mismatches(session)
        if not rows:
            print("ok")
            return 0
        for member_id, token, allowance, purchased, allowance_sum, purchased_sum in rows:
            print(
                f"{member_id} token_balance={token} "
                f"cached={allowance}+{purchased} summed={allowance_sum}+{purchased_sum}"
            )
        return 1
    finally:
        if owns:
            session.close()


if __name__ == "__main__":
    sys.exit(main())
