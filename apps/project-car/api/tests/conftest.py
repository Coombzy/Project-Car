from __future__ import annotations

import os
from datetime import datetime, timedelta
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.auth import clear_login_failures
from app.db import get_db
from app.main import app
from app.models import Base, MembershipTier
from app.shop_time import SHOP_TZ, shop_now

AUTH = {"Authorization": "Bearer dev-owner-secret"}


def seed_placeholder_tiers(session) -> None:
    if session.get(MembershipTier, "basic") is not None:
        return
    for row in (
        MembershipTier(
            name="basic",
            display_name="Basic",
            price=Decimal("150.00"),
            included_tokens=1000,
            booking_window_days=14,
            max_simultaneous_bookings=1,
            notes="Placeholder",
        ),
        MembershipTier(
            name="premium",
            display_name="Premium",
            price=Decimal("250.00"),
            included_tokens=1500,
            booking_window_days=21,
            max_simultaneous_bookings=2,
            notes="Placeholder",
        ),
    ):
        session.add(row)
    session.commit()


@pytest.fixture(autouse=True)
def _shop_clock_on_the_hour(monkeypatch: pytest.MonkeyPatch) -> None:
    """New bookings sit on the hour. Freeze there so ``shop_now() + N hours`` does too."""
    top = datetime.now(SHOP_TZ).replace(minute=0, second=0, microsecond=0)
    monkeypatch.setenv("SHOP_NOW", top.isoformat())


def freeze_shop_clock(at: datetime) -> None:
    os.environ["SHOP_NOW"] = at.isoformat()


def align_booking_start(hours: float = 0) -> datetime:
    """Whole shop hour at least ``hours`` ahead. Still on the hour if the clock is not."""
    now = shop_now()
    start = (now + timedelta(hours=hours)).replace(minute=0, second=0, microsecond=0)
    if start <= now:
        start += timedelta(hours=1)
    return start


def next_grid_start(hours: int = 1) -> datetime:
    return align_booking_start(hours)


def check_in_open_window(length_hours: float = 2) -> tuple[str, str]:
    """An on-the-hour start whose 15-minute check-in window is already open."""
    start = align_booking_start(1)
    freeze_shop_clock(start - timedelta(minutes=10))
    end = start + timedelta(hours=length_hours)
    return start.isoformat(), end.isoformat()


@pytest.fixture(autouse=True)
def _clear_login_failures():
    """Login lockout is one in-process bucket per client IP. Tests share an IP."""
    clear_login_failures()
    yield
    clear_login_failures()


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
