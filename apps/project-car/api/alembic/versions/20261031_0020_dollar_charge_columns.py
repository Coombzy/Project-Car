"""Dollar rows store before-tax, GST, total, and a payment id.

Revision ID: 20261031_0020
Revises: 20261031_0019
Create Date: 2026-10-31

Old manual rows keep a null tax breakdown. New pack and deposit rows fill it.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20261031_0020"
down_revision: Union[str, Sequence[str], None] = "20261031_0019"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("billing_transactions", sa.Column("subtotal_cad", sa.Numeric(10, 2), nullable=True))
    op.add_column("billing_transactions", sa.Column("gst_cad", sa.Numeric(10, 2), nullable=True))
    op.add_column("billing_transactions", sa.Column("total_cad", sa.Numeric(10, 2), nullable=True))
    op.add_column("billing_transactions", sa.Column("gst_rate", sa.Numeric(6, 4), nullable=True))
    op.add_column("billing_transactions", sa.Column("payment_id", sa.String(length=120), nullable=True))
    op.create_index(
        "uq_billing_transactions_payment_id",
        "billing_transactions",
        ["payment_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("uq_billing_transactions_payment_id", table_name="billing_transactions")
    op.drop_column("billing_transactions", "payment_id")
    op.drop_column("billing_transactions", "gst_rate")
    op.drop_column("billing_transactions", "total_cad")
    op.drop_column("billing_transactions", "gst_cad")
    op.drop_column("billing_transactions", "subtotal_cad")
