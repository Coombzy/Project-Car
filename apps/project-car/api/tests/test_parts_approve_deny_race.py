"""PC-AUD-031: one parts approve and one deny, exactly one winner on Postgres."""

from __future__ import annotations

import os
import threading
import uuid
from collections.abc import Iterator

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, func, select, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool

from app.auth import Principal
from app.config import settings
from app.db import get_db
from app.main import app
from app.models import Base, StaffAction
from app.services.staff import decide_parts_request
from tests.conftest import AUTH, create_member, seed_placeholder_tiers
from tests.race import race

pytestmark = pytest.mark.skipif(
    not os.environ.get("TEST_DATABASE_URL", "").startswith("postgresql"),
    reason="needs TEST_DATABASE_URL",
)


@pytest.fixture
def pg_client() -> Iterator[TestClient]:
    url = os.environ["TEST_DATABASE_URL"]
    schema = "aud031_" + uuid.uuid4().hex[:12]
    admin = create_engine(url, poolclass=NullPool)
    engine = create_engine(
        url,
        poolclass=NullPool,
        connect_args={"options": f"-csearch_path={schema}"},
    )
    try:
        with admin.begin() as conn:
            conn.execute(text(f'CREATE SCHEMA "{schema}"'))
        Base.metadata.create_all(engine)
        factory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
        setup = factory()
        try:
            seed_placeholder_tiers(setup)
        finally:
            setup.close()

        def override_db():
            session = factory()
            try:
                yield session
                session.commit()
            except Exception:
                session.rollback()
                raise
            finally:
                session.close()

        app.dependency_overrides[get_db] = override_db
        with TestClient(app) as client:
            client.session_factory = factory  # type: ignore[attr-defined]
            yield client
    finally:
        app.dependency_overrides.pop(get_db, None)
        engine.dispose()
        with admin.begin() as conn:
            conn.execute(text(f'DROP SCHEMA IF EXISTS "{schema}" CASCADE'))
        admin.dispose()


def test_parts_approve_deny_has_one_winner(pg_client: TestClient) -> None:
    member = create_member(pg_client, email="ada.aud031@example.com")
    created = pg_client.post(
        "/parts-requests",
        headers=AUTH,
        json={"member_id": member["id"], "sku": "PT-OIL-5W30-012", "note": "race"},
    )
    assert created.status_code == 201, created.text
    request_id = uuid.UUID(created.json()["id"])
    principal = Principal(role="owner", email=settings.owner_email)
    sides = [True, False]
    lock = threading.Lock()

    def call(session: Session) -> tuple[int, str | None]:
        with lock:
            approve = sides.pop()
        try:
            decide_parts_request(session, request_id, principal, approve=approve)
            session.commit()
            return 200, None
        except HTTPException as exc:
            session.rollback()
            detail = exc.detail if isinstance(exc.detail, dict) else {}
            return exc.status_code, detail.get("code")

    results, errors = race(2, call, pg_client.session_factory)
    assert errors == [None, None], errors
    codes = sorted(status for status, _code in results)
    assert codes == [200, 409], results
    assert any(code == "request_already_decided" for _status, code in results)
    session = pg_client.session_factory()
    try:
        count = session.scalar(
            select(func.count())
            .select_from(StaffAction)
            .where(StaffAction.request_id == request_id)
        )
    finally:
        session.close()
    assert count == 1
