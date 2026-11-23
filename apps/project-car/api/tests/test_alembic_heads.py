"""Alembic has one head and can upgrade a database that has no tables yet."""

from __future__ import annotations

from pathlib import Path

from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, text

ALEMBIC_INI = Path(__file__).resolve().parents[1] / "alembic.ini"
HEAD = "20261031_0019"


def test_alembic_has_a_single_head() -> None:
    script = ScriptDirectory.from_config(Config(str(ALEMBIC_INI)))
    assert script.get_heads() == [HEAD]


def test_upgrade_runs_from_an_empty_db(tmp_path: Path, monkeypatch) -> None:
    db_path = tmp_path / "empty.db"
    url = f"sqlite:///{db_path}"
    from app.config import settings

    # env.py replaces sqlalchemy.url with settings.database_url on import.
    monkeypatch.setattr(settings, "database_url", url)
    config = Config(str(ALEMBIC_INI))
    config.set_main_option("script_location", str(ALEMBIC_INI.parent / "alembic"))
    config.set_main_option("sqlalchemy.url", url)

    command.upgrade(config, "head")

    engine = create_engine(url)
    try:
        with engine.connect() as connection:
            heads = connection.execute(text("SELECT version_num FROM alembic_version")).scalars().all()
    finally:
        engine.dispose()
    assert heads == [HEAD]
