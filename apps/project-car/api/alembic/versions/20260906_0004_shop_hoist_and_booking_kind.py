"""Shop hoist flag and booking kind (customer vs shop).

Revision ID: 20260906_0004
Revises: 20260906_0003
Create Date: 2026-09-06
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260906_0004"
down_revision: Union[str, Sequence[str], None] = "20260906_0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "hoists",
        sa.Column("is_shop", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "bookings",
        sa.Column("kind", sa.String(length=32), nullable=False, server_default="customer"),
    )
    op.alter_column(
        "bookings",
        "member_id",
        existing_type=postgresql.UUID(as_uuid=True),
        nullable=True,
    )
    op.alter_column("hoists", "is_shop", server_default=None)
    op.alter_column("bookings", "kind", server_default=None)


def downgrade() -> None:
    op.alter_column(
        "bookings",
        "member_id",
        existing_type=postgresql.UUID(as_uuid=True),
        nullable=False,
    )
    op.drop_column("bookings", "kind")
    op.drop_column("hoists", "is_shop")
