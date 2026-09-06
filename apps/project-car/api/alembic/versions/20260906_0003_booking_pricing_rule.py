"""Store pricing_rule on bookings and ledger meta.

Revision ID: 20260906_0003
Revises: 20260906_0002
Create Date: 2026-09-06
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260906_0003"
down_revision: Union[str, Sequence[str], None] = "20260906_0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pricing = sa.JSON().with_variant(postgresql.JSONB(), "postgresql")
    op.add_column("bookings", sa.Column("pricing_rule", pricing, nullable=True))
    op.add_column("token_transactions", sa.Column("meta", pricing, nullable=True))


def downgrade() -> None:
    op.drop_column("token_transactions", "meta")
    op.drop_column("bookings", "pricing_rule")
