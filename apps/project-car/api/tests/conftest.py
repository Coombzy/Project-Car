from __future__ import annotations

import os
from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.auth import clear_login_failures
from app.db import get_db
from app.main import app
from app.models import Base, MembershipTier
from app.seed import PLACEHOLDER_TIERS
from app.shop_time import shop_now

AUTH = {"Authorization": "Bearer dev-owner-secret"}


def seed_placeholder_tiers(session) -> None:
    if session.get(MembershipTier, "basic") is not None:
        return
    for payload in PLACEHOLDER_TIERS:
        session.add(MembershipTier(**payload))
    session.commit()


@pytest.fixture(autouse=True)
def _clear_login_failures():
    """Login lockout is one in-process bucket per client IP. Tests share an IP."""
    clear_login_failures()
    yield
    clear_login_failures()


@pytest.fixture(autouse=True)
def _restore_shop_clock(monkeypatch: pytest.MonkeyPatch):
    """``freeze_shop_clock`` writes SHOP_NOW directly; undo puts it back after each test."""
    monkeypatch.setenv("SHOP_NOW", os.environ.get("SHOP_NOW", ""))
    yield


def next_hour(hours: float = 0) -> datetime:
    """Start of the next whole shop hour, plus ``hours``. New bookings sit on the hour."""
    top = shop_now().replace(minute=0, second=0, microsecond=0)
    return top + timedelta(hours=1 + hours)


def freeze_shop_clock(at: datetime) -> None:
    os.environ["SHOP_NOW"] = at.isoformat()


def check_in_open_start() -> datetime:
    """An on-the-hour start whose 15-minute check-in window is already open.

    Freezes the shop clock 10 minutes before that start for the rest of the test.
    """
    start = next_hour()
    freeze_shop_clock(start - timedelta(minutes=10))
    return start


@pytest.fixture
def client() -> TestClient:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    TestingSession = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

    setup = TestingSession()
    seed_placeholder_tiers(setup)
    setup.close()

    def override_db():
        session = TestingSession()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_db
    with TestClient(app) as test_client:
        test_client.session_factory = TestingSession  # type: ignore[attr-defined]
        yield test_client
    app.dependency_overrides.clear()


def create_member(client: TestClient, **overrides) -> dict:
    payload = {
        "name": "Ada Reyes",
        "email": "ada@example.com",
        "tier_name": "premium",
        **overrides,
    }
    response = client.post("/members", json=payload, headers=AUTH)
    assert response.status_code == 201, response.text
    return response.json()


def login_member(client: TestClient, email: str, password: str = "changeme") -> dict:
    response = client.post("/auth/member/login", json={"email": email, "password": password})
    assert response.status_code == 200, response.text
    return response.json()


def create_hoist(client: TestClient, **overrides) -> dict:
    payload = {"name": "Bay 1", "location_label": "North wall", **overrides}
    response = client.post("/hoists", json=payload, headers=AUTH)
    assert response.status_code == 201, response.text
    return response.json()
