"""Pool rules for app.db._create_engine: shared memory sqlite, pooled file sqlite, pinging postgres."""

from unittest.mock import patch

import app.db as db
from app.db import _create_engine
from sqlalchemy.pool import QueuePool, StaticPool


def _build(url: str):
    """Run _create_engine for url and return its engine plus create_engine kwargs.

    create_engine is lazy, so no connection is opened for any url.
    """
    calls: list[dict] = []
    real = db.create_engine

    def spy(*args, **kwargs):
        calls.append(kwargs)
        return real(*args, **kwargs)

    with patch.object(db, "create_engine", spy), patch.object(
        db.settings, "database_url", url
    ):
        engine = _create_engine()
    return engine, calls[0]


def test_memory_sqlite_uses_static_pool():
    for url in ("sqlite://", "sqlite:///:memory:"):
        engine, kwargs = _build(url)
        try:
            assert type(engine.pool) is StaticPool
            assert kwargs["poolclass"] is StaticPool
            assert kwargs["connect_args"] == {"check_same_thread": False}
            assert engine.pool._pre_ping is False
        finally:
            engine.dispose()


def test_file_sqlite_uses_default_pool():
    engine, kwargs = _build("sqlite:///./visual-check.db")
    try:
        assert isinstance(engine.pool, QueuePool)
        assert not isinstance(engine.pool, StaticPool)
        assert "poolclass" not in kwargs
        assert kwargs["connect_args"] == {"check_same_thread": False}
        assert engine.pool._pre_ping is False
    finally:
        engine.dispose()


def test_postgres_url_sets_pool_pre_ping():
    engine, kwargs = _build("postgresql://u:p@127.0.0.1:9/db")
    try:
        assert engine.pool._pre_ping is True
        assert kwargs["pool_pre_ping"] is True
        assert isinstance(engine.pool, QueuePool)
    finally:
        engine.dispose()
