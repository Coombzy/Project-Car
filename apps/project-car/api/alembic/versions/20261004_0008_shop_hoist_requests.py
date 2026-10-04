"""Shop hoist requests. A pending request is not a booking.

Revision ID: 20261004_0008
Revises: 20260906_0007
Create Date: 2026-10-04
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20261004_0008"
down_revision: Union[str, Sequence[str], None] = "20260906_0007"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pricing = sa.JSON().with_variant(postgresql.JSONB(), "postgresql")
    op.create_table(
        "shop_hoist_requests",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("member_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("hoist_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("start_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("token_quote", sa.Numeric(12, 2), nullable=False),
        sa.Column("pricing_rule", pricing, nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_by_kind", sa.String(length=32), nullable=False),
        sa.Column("created_by_id", sa.String(length=320), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["hoist_id"], ["hoists.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["member_id"], ["members.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_shop_hoist_requests_hoist_status",
        "shop_hoist_requests",
        ["hoist_id", "status"],
    )
    op.create_index("ix_shop_hoist_requests_member", "shop_hoist_requests", ["member_id"])


def downgrade() -> None:
    op.drop_index("ix_shop_hoist_requests_member", table_name="shop_hoist_requests")
    op.drop_index("ix_shop_hoist_requests_hoist_status", table_name="shop_hoist_requests")
    op.drop_table("shop_hoist_requests")
