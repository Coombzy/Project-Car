"""Four band labels rename. Saved multipliers stay.

Red on main: 20261031_0018 is not in the chain after 20261105_0019,
so the Off-peak, Normal, Evening, and Peak labels are absent.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

from alembic.config import Config
from alembic.operations import Operations
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, text

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "alembic/versions/20261031_0018_four_band_labels.py"
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
    spec = importlib.util.spec_from_file_location("four_band_labels", PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _rows(connection):
    return connection.execute(
        text("SELECT id, label, multiplier, sort_order FROM pricing_bands ORDER BY id")
    ).all()


def test_four_band_labels_follow_signup_and_keep_multipliers() -> None:
    script = ScriptDirectory.from_config(Config(str(ROOT / "alembic.ini")))
    by_id = {item.revision: item for item in script.walk_revisions()}
    assert "20261031_0018" in by_id
    assert by_id["20261031_0018"].down_revision == "20261105_0019"
    assert script.get_heads() == ["20261031_0018"]

    module = _load()
    assert module.revision == "20261031_0018" and module.down_revision == "20261105_0019"
    assert module.LABELS == LABELS

    engine = create_engine("sqlite://")
    with engine.begin() as connection:
        connection.execute(text(
            "CREATE TABLE pricing_bands (id VARCHAR(64) PRIMARY KEY, "
            "label VARCHAR(120) NOT NULL, multiplier NUMERIC NOT NULL, sort_order INTEGER NOT NULL)"
        ))
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
        before = _rows(connection)

        def apply(fn) -> None:
            with Operations.context(MigrationContext.configure(connection)):
                fn()

        apply(module.upgrade)
        renamed = {row[0]: row for row in _rows(connection)}
        saved = {row[0]: row for row in before}
        for band_id, label, order in LABELS:
            assert renamed[band_id][1] == label
            assert renamed[band_id][3] == order
            assert renamed[band_id][2] == saved[band_id][2]
        apply(module.downgrade)
        assert _rows(connection) == before
