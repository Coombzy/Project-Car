"""Shop-wide signup mode. Self-serve is the default; waitlist is the fallback.

Revision ID: 20261031_0022
Revises: 20261031_0021
Create Date: 2026-10-31
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20261031_0022"
down_revision: Union[str, Sequence[str], None] = "20261031_0021"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "shop_settings",
        sa.Column("key", sa.String(length=64), nullable=False),
        sa.Column("value", sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint("key"),
    )
    op.execute(
        sa.text("INSERT INTO shop_settings (key, value) VALUES ('signup_mode', 'self_serve')")
    )


def downgrade() -> None:
    op.drop_table("shop_settings")
