"""Track allowance and purchased tokens separately.

Revision ID: 20261105_0018
Revises: 20261105_0017
Create Date: 2026-11-05

Backfill rule: a token_purchase row copies amount onto purchased_amount and
sets allowance_amount to 0. Every other kind copies amount onto
allowance_amount and sets purchased_amount to 0. Each member's
allowance_balance and purchased_balance are the sums of those columns.
token_balance is left as stored. When that cache already equals the ledger
sum, the two piles add up to it, because each row's amount lands in exactly
one pile. A cache that had drifted stays drifted until the next ledger write
or rebuild.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20261105_0018"
down_revision: Union[str, Sequence[str], None] = "20261105_0017"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "members",
        sa.Column("allowance_balance", sa.Numeric(12, 2), nullable=False, server_default="0"),
    )
    op.add_column(
        "members",
        sa.Column("purchased_balance", sa.Numeric(12, 2), nullable=False, server_default="0"),
    )
    op.add_column(
        "token_transactions",
        sa.Column("allowance_amount", sa.Numeric(12, 2), nullable=False, server_default="0"),
    )
    op.add_column(
        "token_transactions",
        sa.Column("purchased_amount", sa.Numeric(12, 2), nullable=False, server_default="0"),
    )
    op.execute(
        """
        UPDATE token_transactions
        SET purchased_amount = amount, allowance_amount = 0
        WHERE kind = 'token_purchase'
        """
    )
    op.execute(
        """
        UPDATE token_transactions
        SET allowance_amount = amount, purchased_amount = 0
        WHERE kind != 'token_purchase'
        """
    )
    op.execute(
        """
        UPDATE members
        SET allowance_balance = (
                SELECT COALESCE(SUM(allowance_amount), 0)
                FROM token_transactions
                WHERE token_transactions.member_id = members.id
            ),
            purchased_balance = (
                SELECT COALESCE(SUM(purchased_amount), 0)
                FROM token_transactions
                WHERE token_transactions.member_id = members.id
            )
        """
    )


def downgrade() -> None:
    op.drop_column("token_transactions", "purchased_amount")
    op.drop_column("token_transactions", "allowance_amount")
    op.drop_column("members", "purchased_balance")
    op.drop_column("members", "allowance_balance")
