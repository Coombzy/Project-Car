"""Demo Owner seed is loopback-only."""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import DEMO_OWNER_EMAIL, DEMO_OWNER_PASSWORD, Settings
from app.db import get_db
from app.main import app
from app.seed import main, seed
from app.seed_guard import (
    DemoOwnerSeedRefused,
    database_host,
    is_loopback_host,
    refuse_demo_owner_off_loopback,
)

_REMOTE_URL = "postgresql+psycopg://projectcar:projectcar@203.0.113.10:5432/projectcar?connect_timeout=1"
_QUERY_HOST_URL = "postgresql+psycopg://projectcar:projectcar@/projectcar?host=203.0.113.10&connect_timeout=1"

_PUBLIC_READMES = (
    "README.md",
    "apps/project-car/web/README.md",
    "apps/project-car/api/README.md",
)


def _demo_settings(**overrides: str) -> Settings:
    values: dict[str, str] = {
        "owner_email": DEMO_OWNER_EMAIL,
        "owner_password": DEMO_OWNER_PASSWORD,
        "database_url": "postgresql+psycopg://projectcar:projectcar@127.0.0.1:5432/projectcar",
    }
    values.update(overrides)
    return Settings(**values)


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "apps" / "project-car" / "api" / "app" / "seed.py").is_file():
            return parent
    raise RuntimeError("repo root not found")


def test_demo_owner_constants_are_the_settings_defaults() -> None:
    assert Settings.model_fields["owner_email"].default == DEMO_OWNER_EMAIL
    assert Settings.model_fields["owner_password"].default == DEMO_OWNER_PASSWORD


def test_public_readmes_omit_demo_owner_password() -> None:
    root = _repo_root()
    for rel in _PUBLIC_READMES:
        text = (root / rel).read_text(encoding="utf-8")
        assert DEMO_OWNER_PASSWORD not in text, rel
        assert f"{DEMO_OWNER_EMAIL} / {DEMO_OWNER_PASSWORD}" not in text, rel


def test_host_classification() -> None:
    assert is_loopback_host(None)
    assert is_loopback_host("")
    assert is_loopback_host("localhost")
    assert is_loopback_host("LOCALHOST")
    assert is_loopback_host("127.0.0.1")
    assert is_loopback_host("127.8.8.8")
    assert is_loopback_host("::1")
    assert database_host("sqlite://") is None
    assert is_loopback_host(database_host("postgresql+psycopg://u:p@localhost:5432/db"))
    assert is_loopback_host(database_host("postgresql+psycopg://u:p@127.0.0.1:5432/db"))
    assert is_loopback_host(database_host("postgresql+psycopg://u:p@[::1]:5432/db"))
    assert is_loopback_host(database_host("postgresql+psycopg://u:p@/db?host=/var/run/postgresql"))
    assert not is_loopback_host("0.0.0.0")
    assert not is_loopback_host("203.0.113.10")
    assert not is_loopback_host(database_host(_REMOTE_URL))
    assert not is_loopback_host(database_host(_QUERY_HOST_URL))


def test_guard_refuses_only_the_demo_pair_off_loopback() -> None:
    with pytest.raises(DemoOwnerSeedRefused):
        refuse_demo_owner_off_loopback("203.0.113.10", DEMO_OWNER_EMAIL, DEMO_OWNER_PASSWORD)
    with pytest.raises(DemoOwnerSeedRefused):
        refuse_demo_owner_off_loopback("203.0.113.10", "Owner@ProjectCar.ca", DEMO_OWNER_PASSWORD)
    refuse_demo_owner_off_loopback("127.0.0.1", DEMO_OWNER_EMAIL, DEMO_OWNER_PASSWORD)
    refuse_demo_owner_off_loopback("localhost", DEMO_OWNER_EMAIL, DEMO_OWNER_PASSWORD)
    refuse_demo_owner_off_loopback("::1", DEMO_OWNER_EMAIL, DEMO_OWNER_PASSWORD)
    refuse_demo_owner_off_loopback(None, DEMO_OWNER_EMAIL, DEMO_OWNER_PASSWORD)
    refuse_demo_owner_off_loopback("203.0.113.10", DEMO_OWNER_EMAIL, "a-different-secret")
    refuse_demo_owner_off_loopback("203.0.113.10", "owner@example.com", DEMO_OWNER_PASSWORD)


def test_seed_refuses_demo_owner_off_loopback(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("app.seed.get_settings", lambda: _demo_settings(database_url=_REMOTE_URL))
    engine = create_engine(_REMOTE_URL)
    remote_session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    session = remote_session()
    try:
        with pytest.raises(DemoOwnerSeedRefused):
            seed(session, reset=True)
    finally:
        session.close()
        engine.dispose()


def test_seed_refuses_demo_owner_when_host_is_only_in_the_query(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("app.seed.get_settings", lambda: _demo_settings(database_url=_QUERY_HOST_URL))
    engine = create_engine(_QUERY_HOST_URL)
    remote_session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    session = remote_session()
    try:
        with pytest.raises(DemoOwnerSeedRefused):
            seed(session, reset=False)
    finally:
        session.close()
        engine.dispose()


def test_loopback_seed_still_runs(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("app.seed.get_settings", lambda: _demo_settings())
    session_gen = app.dependency_overrides[get_db]()
    session = next(session_gen)
    try:
        summary = seed(session, reset=True)
        session.commit()
    finally:
        session_gen.close()
    assert summary["members"] == 6
    assert summary["hoists"] == 6
    assert summary["bookings"] >= 6


def test_main_refuses_off_loopback_without_connecting(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr("app.seed.get_settings", lambda: _demo_settings(database_url=_REMOTE_URL))

    def fail_connect() -> None:
        raise AssertionError("seed opened a connection")

    monkeypatch.setattr("app.seed.SessionLocal", fail_connect)
    assert main([]) == 1
    captured = capsys.readouterr()
    assert "loopback" in captured.err
    assert DEMO_OWNER_PASSWORD not in captured.err
    assert DEMO_OWNER_PASSWORD not in captured.out


def test_main_still_reaches_seed_on_loopback(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr("app.seed.get_settings", lambda: _demo_settings())
    called = {"seed": False}

    class FakeSession:
        def commit(self) -> None:
            return None

        def rollback(self) -> None:
            return None

        def close(self) -> None:
            return None

    monkeypatch.setattr("app.seed.SessionLocal", lambda: FakeSession())

    def fake_seed(session: object, *, reset: bool = False) -> dict[str, int]:
        called["seed"] = True
        assert reset is False
        return {
            "members": 6,
            "hoists": 6,
            "bookings": 7,
            "todos": 6,
            "parts_orders": 3,
            "chat_rooms": 1,
            "waitlist": 4,
            "tiers": 2,
        }

    monkeypatch.setattr("app.seed.seed", fake_seed)
    assert main([]) == 0
    assert called["seed"] is True
    captured = capsys.readouterr()
    assert "Shop OS demo data ready" in captured.out
    assert DEMO_OWNER_PASSWORD not in captured.out
    assert DEMO_OWNER_PASSWORD not in captured.err
