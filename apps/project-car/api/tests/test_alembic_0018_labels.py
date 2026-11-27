"""Rename the four pricing band labels. A saved multiplier stays put.

Red on main: revision 20261031_0018 is missing, so the chain from
20261105_0019 does not include that revision and the four new labels
are absent.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

from alembic.config import Config
from alembic.operations import Operations
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, text

API_ROOT = Path(__file__).resolve().parents[1]
VERSIONS = API_ROOT / "alembic" / "versions"
ALEMBIC_INI = API_ROOT / "alembic.ini"
REVISION_PATH = VERSIONS / "20261031_0018_four_band_labels.py"

# Owner-edited multipliers. They differ from the 20261014_0013 seeds on purpose.
SAVED = (
    ("late_night", "Late night / early morning", "0.5500", 3),
    ("weekday_day", "Weekday day (base)", "1.0500", 0),
    ("weekday_eve", "Weekday evening", "1.3500", 1),
    ("weekend_fri_eve", "Weekend / Fri eve", "1.6500", 2),
)
LABELS = (
    ("late_night", "Off-peak", 0),
    ("weekday_day", "Normal", 1),
    ("weekday_eve", "Evening", 2),
    ("weekend_fri_eve", "Peak", 3),
)


def _load():
    assert REVISION_PATH.is_file(), REVISION_PATH
    spec = importlib.util.spec_from_file_location("four_band_labels", REVISION_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _bands(connection) -> dict[str, tuple]:
    rows = connection.execute(
        text("SELECT id, label, multiplier, sort_order FROM pricing_bands ORDER BY id")
    ).all()
    return {row[0]: (row[1], row[2], row[3]) for row in rows}


def _apply(connection, fn) -> None:
    with Operations.context(MigrationContext.configure(connection)):
        fn()


def test_four_band_labels_follow_signup_and_keep_multipliers() -> None:
    script = ScriptDirectory.from_config(Config(str(ALEMBIC_INI)))
    revision = script.get_revision("20261031_0018")
    assert revision is not None
    assert revision.down_revision == "20261105_0019"
    assert script.get_heads() == ["20261031_0018"]

    module = _load()
    assert module.revision == "20261031_0018"
    assert module.down_revision == "20261105_0019"
    assert module.LABELS == LABELS

    engine = create_engine("sqlite://")
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                CREATE TABLE pricing_bands (
                    id VARCHAR(64) PRIMARY KEY,
                    label VARCHAR(120) NOT NULL,
                    multiplier NUMERIC NOT NULL,
                    sort_order INTEGER NOT NULL
                )
                """
            )
        )
        connection.execute(
            text(
                "INSERT INTO pricing_bands (id, label, multiplier, sort_order) "
                "VALUES (:id, :label, :multiplier, :sort_order)"
            ),
            [
                {"id": band_id, "label": label, "multiplier": multiplier, "sort_order": order}
                for band_id, label, multiplier, order in SAVED
            ],
        )
        connection.execute(
            text(
                "INSERT INTO pricing_bands (id, label, multiplier, sort_order) "
                "VALUES ('owner_extra', 'Owner extra', '9.0000', 9)"
            )
        )
        before = _bands(connection)
        _apply(connection, module.upgrade)
        renamed = _bands(connection)
        for band_id, label, order in LABELS:
            assert renamed[band_id][0] == label
            assert renamed[band_id][2] == order
            assert renamed[band_id][1] == before[band_id][1]
        assert renamed["owner_extra"] == before["owner_extra"]
        _apply(connection, module.downgrade)
        assert _bands(connection) == before
