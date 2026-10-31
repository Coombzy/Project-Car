"""Track allowance and purchased tokens separately.

Revision ID: 20261031_0021
Revises: 20261031_0020
Create Date: 2026-10-31

Existing purchases are credited to the purchased pile. Every other ledger row
is treated as allowance. A shop that is not open has not spent a real pack.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20261031_0021"
down_revision: Union[str, Sequence[str], None] = "20261031_0020"
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
