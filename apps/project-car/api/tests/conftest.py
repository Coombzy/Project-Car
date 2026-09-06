from __future__ import annotations

from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import get_db
from app.main import app
from app.models import Base, MembershipTier

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


def create_hoist(client: TestClient, **overrides) -> dict:
    payload = {"name": "Bay 1", "location_label": "North wall", **overrides}
    response = client.post("/hoists", json=payload, headers=AUTH)
    assert response.status_code == 201, response.text
    return response.json()
