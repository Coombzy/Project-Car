"""Member parts requests.

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
    op.create_table(
        "parts_requests",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("member_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("sku", sa.String(length=80), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["member_id"], ["members.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_parts_requests_member_created",
        "parts_requests",
        ["member_id", "created_at"],
    )
    op.create_index(
        "ix_parts_requests_status_created",
        "parts_requests",
        ["status", "created_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_parts_requests_status_created", table_name="parts_requests")
    op.drop_index("ix_parts_requests_member_created", table_name="parts_requests")
    op.drop_table("parts_requests")
