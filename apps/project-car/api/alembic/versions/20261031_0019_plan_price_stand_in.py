"""Move leftover demo tier prices to the CAD stand-ins.

Revision ID: 20261031_0019
Revises: 20261031_0018
Create Date: 2026-10-31

Basic becomes 500 CAD/month and Premium becomes 750 only when the row is
still the previous demo price. An owner edit is left alone. Placeholder
notes pick up the Premium stand-in mark. A custom note is left alone.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from app.services.plan_price import tier_notes

revision: str = "20261031_0019"
down_revision: Union[str, Sequence[str], None] = "20261031_0018"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_PRICE = sa.text(
    "UPDATE membership_tiers SET price = :price WHERE name = :name AND price = :previous"
)
_NOTES = sa.text(
    "UPDATE membership_tiers SET notes = :notes "
    "WHERE name = :name AND notes LIKE 'Placeholder. Owner can edit.%'"
)


def upgrade() -> None:
    connection = op.get_bind()
    connection.execute(
        _PRICE,
        {"name": "basic", "price": "500.00", "previous": "150.00"},
    )
    connection.execute(
        _PRICE,
        {"name": "premium", "price": "750.00", "previous": "250.00"},
    )
    connection.execute(
        _NOTES,
        {
            "name": "basic",
            "notes": tier_notes(premium=False, included_tokens=1000, base_tokens_per_hour=100),
        },
    )
    connection.execute(
        _NOTES,
        {
            "name": "premium",
            "notes": tier_notes(premium=True, included_tokens=1500, base_tokens_per_hour=100),
        },
    )


def downgrade() -> None:
    connection = op.get_bind()
    connection.execute(
        _PRICE,
        {"name": "basic", "price": "150.00", "previous": "500.00"},
    )
    connection.execute(
        _PRICE,
        {"name": "premium", "price": "250.00", "previous": "750.00"},
    )
