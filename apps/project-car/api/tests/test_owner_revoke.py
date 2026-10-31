"""Owner logout revokes every owner cookie. A password change does too."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest
from alembic.operations import Operations
from alembic.runtime.migration import MigrationContext
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect, text

from app.config import get_settings

REVISION = (
    Path(__file__).resolve().parents[1]
    / "alembic"
    / "versions"
    / "20261031_0023_owner_session_epoch.py"
)


def _login(client: TestClient, password: str) -> str:
    settings = get_settings()
    client.cookies.clear()
    response = client.post(
        "/auth/login",
        json={"email": settings.owner_email, "password": password},
    )
    assert response.status_code == 200, response.text
    token = client.cookies.get(settings.cookie_name)
    assert token
    return token


def _replay(client: TestClient, token: str) -> int:
    settings = get_settings()
    client.cookies.clear()
    client.cookies.set(settings.cookie_name, token)
    return client.get("/me").status_code


def test_owner_cookie_rejected_after_logout(client: TestClient) -> None:
    settings = get_settings()
    first = _login(client, settings.owner_password)
    client.cookies.clear()
    second = _login(client, settings.owner_password)
    logged_out = client.post("/auth/logout")
    assert logged_out.status_code == 200, logged_out.text
    assert _replay(client, first) == 401
    assert _replay(client, second) == 401
    bearer = client.get("/me", headers={"Authorization": "Bearer dev-owner-secret"})
    assert bearer.status_code == 200, bearer.text
    fresh = _login(client, settings.owner_password)
    assert _replay(client, fresh) == 200


def test_owner_cookie_rejected_after_password_change(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    settings = get_settings()
    old = _login(client, settings.owner_password)
    assert _replay(client, old) == 200
    monkeypatch.setattr(settings, "owner_password", "a-new-owner-password")
    assert _replay(client, old) == 401
    fresh = _login(client, "a-new-owner-password")
    assert _replay(client, fresh) == 200


def test_owner_session_epoch_migration_roundtrip() -> None:
    spec = importlib.util.spec_from_file_location("owner_session_epoch_20261031_0023", REVISION)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.revision == "20261031_0023"
    assert module.down_revision == "20261031_0022"

    engine = create_engine("sqlite://")
    with engine.begin() as connection:
        context = MigrationContext.configure(connection)
        with Operations.context(context):
            module.upgrade()
        assert "owner_session_epoch" in inspect(connection).get_table_names()
        row = connection.execute(text("SELECT epoch FROM owner_session_epoch")).one()
        assert row[0] == 1
        with Operations.context(context):
            module.downgrade()
        assert "owner_session_epoch" not in inspect(connection).get_table_names()
        with Operations.context(context):
            module.upgrade()
        assert "owner_session_epoch" in inspect(connection).get_table_names()
