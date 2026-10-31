"""Token purchases carry their payment id; one reserve, refund and debit per booking.

Revision ID: 20261031_0017
Revises: 20261023_0016
Create Date: 2026-10-31
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20261031_0017"
down_revision: Union[str, Sequence[str], None] = "20261023_0016"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

ONCE_PER_BOOKING = (
    "booking_id IS NOT NULL AND kind IN ('booking_reserve', 'booking_refund', 'booking_debit')"
)


def upgrade() -> None:
    op.add_column(
        "token_transactions",
        sa.Column("payment_ref", sa.String(length=120), nullable=True),
    )
    op.create_index(
        "uq_token_transactions_payment_ref",
        "token_transactions",
        ["payment_ref"],
        unique=True,
    )
    # Existing data writes at most one of each per booking. A duplicate fails
    # the upgrade here, so it must be reconciled by hand first.
    op.create_index(
        "uq_token_transactions_booking_kind",
        "token_transactions",
        ["booking_id", "kind"],
        unique=True,
        sqlite_where=sa.text(ONCE_PER_BOOKING),
        postgresql_where=sa.text(ONCE_PER_BOOKING),
    )


def downgrade() -> None:
    op.drop_index("uq_token_transactions_booking_kind", table_name="token_transactions")
    op.drop_index("uq_token_transactions_payment_ref", table_name="token_transactions")
    op.drop_column("token_transactions", "payment_ref")
