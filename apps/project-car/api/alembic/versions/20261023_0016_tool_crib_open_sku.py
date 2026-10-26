"""One open crib checkout per SKU.

Revision ID: 20261023_0016
Revises: 20261016_0015
Create Date: 2026-10-23
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20261023_0016"
down_revision: Union[str, Sequence[str], None] = "20261016_0015"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "tool_crib_events",
        sa.Column("open_sku", sa.String(length=80), nullable=True),
    )
    # Open checkout = a checkout row nothing has returned. At most one per SKU
    # in data this revision expects. A second open row fails the unique index.
    op.execute(
        """
        UPDATE tool_crib_events
        SET open_sku = sku
        WHERE kind = 'checkout'
          AND NOT EXISTS (
            SELECT 1
            FROM tool_crib_events AS returned
            WHERE returned.checkout_id = tool_crib_events.id
          )
        """
    )
    op.create_index(
        "uq_tool_crib_events_open_sku",
        "tool_crib_events",
        ["open_sku"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("uq_tool_crib_events_open_sku", table_name="tool_crib_events")
    op.drop_column("tool_crib_events", "open_sku")
