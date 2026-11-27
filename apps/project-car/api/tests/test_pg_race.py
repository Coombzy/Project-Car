"""SQLite checks that race() releases workers together. No Postgres marker."""

import threading
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from tests.race import race


def _session_factory():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    return sessionmaker(bind=engine)


def test_race_helper_releases_together():
    n = 8

    def fn(session):
        stamp = time.perf_counter()
        assert session is not None
        return stamp

    results, exceptions = race(n, fn, _session_factory())
    assert exceptions == [None] * n
    assert all(isinstance(stamp, float) for stamp in results)
    assert max(results) - min(results) < 0.5


def test_race_captures_a_worker_exception():
    lock = threading.Lock()
    state = {"seen": 0}

    def fn(session):
        assert session is not None
        with lock:
            state["seen"] += 1
            mine = state["seen"]
        if mine == 1:
            raise RuntimeError("worker failed")
        return mine

    results, exceptions = race(4, fn, _session_factory())
    assert sum(isinstance(exc, RuntimeError) for exc in exceptions) == 1
    assert any(exc is not None and str(exc) == "worker failed" for exc in exceptions)
    assert sum(value is not None for value in results) == 3
    assert {value for value in results if value is not None} == {2, 3, 4}
