"""Link a converted waitlist row to the member it created.

Revision ID: 20261014_0014
Revises: 20261014_0013
Create Date: 2026-10-14
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20261014_0014"
down_revision: Union[str, Sequence[str], None] = "20261014_0013"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "waitlist_entries",
        sa.Column("member_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        "fk_waitlist_entries_member_id",
        "waitlist_entries",
        "members",
        ["member_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index("ix_waitlist_entries_member_id", "waitlist_entries", ["member_id"])


def downgrade() -> None:
    op.drop_index("ix_waitlist_entries_member_id", table_name="waitlist_entries")
    op.drop_constraint("fk_waitlist_entries_member_id", "waitlist_entries", type_="foreignkey")
    op.drop_column("waitlist_entries", "member_id")
