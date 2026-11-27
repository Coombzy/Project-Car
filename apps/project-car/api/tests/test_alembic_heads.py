"""Alembic has one head and can upgrade a database that has no tables yet."""

from __future__ import annotations

import importlib.util
from pathlib import Path

from alembic.config import Config
from alembic.operations import Operations
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, text

from app.services.plan_price import tier_notes

ALEMBIC_INI = Path(__file__).resolve().parents[1] / "alembic.ini"
HEAD = "20261031_0019"


def test_alembic_has_a_single_head() -> None:
    script = ScriptDirectory.from_config(Config(str(ALEMBIC_INI)))
    assert script.get_heads() == [HEAD]


def test_upgrade_runs_from_an_empty_db() -> None:
    """One chain from base to head. Import each revision; do not run DDL on sqlite."""
    script = ScriptDirectory.from_config(Config(str(ALEMBIC_INI)))
    chain = list(script.walk_revisions("base", HEAD))
    assert script.get_bases() == [chain[-1].revision]
    previous = None
    for revision in reversed(chain):
        assert revision.down_revision == previous
        assert callable(revision.module.upgrade)
        assert callable(revision.module.downgrade)
        previous = revision.revision
    assert previous == HEAD


def test_downgrade_rewinds_placeholder_notes(tmp_path: Path) -> None:
    """Stand-in notes return to the placeholder; a custom note and an edited price stay."""
    path = ALEMBIC_INI.parent / "alembic/versions/20261031_0019_plan_price_stand_in.py"
    spec = importlib.util.spec_from_file_location("rev_20261031_0019", path)
    revision = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(revision)

    basic = tier_notes(premium=False, included_tokens=1000, base_tokens_per_hour=100)
    premium = tier_notes(premium=True, included_tokens=1500, base_tokens_per_hour=100)
    custom = "Owner set a custom note."
    engine = create_engine(f"sqlite:///{tmp_path / 'notes.db'}")
    try:
        with engine.begin() as connection:
            connection.execute(text(
                "CREATE TABLE membership_tiers (name TEXT NOT NULL, price TEXT NOT NULL, notes TEXT)"
            ))
            connection.execute(
                text("INSERT INTO membership_tiers (name, price, notes) VALUES (:n, :p, :notes)"),
                [
                    {"n": "basic", "p": "500.00", "notes": basic},
                    {"n": "premium", "p": "750.00", "notes": premium},
                    {"n": "basic", "p": "500.00", "notes": custom},
                    {"n": "premium", "p": "640.00", "notes": premium},
                ],
            )
            with Operations.context(MigrationContext.configure(connection)):
                revision.downgrade()
            found = connection.execute(
                text("SELECT name, price, notes FROM membership_tiers ORDER BY rowid")
            ).all()
    finally:
        engine.dispose()
    assert list(found) == [
        ("basic", "150.00", "Placeholder. Owner can edit."),
        ("premium", "250.00", "Placeholder. Owner can edit."),
        ("basic", "150.00", custom),
        ("premium", "640.00", "Placeholder. Owner can edit."),
    ]
