"""PC-AUD-031: one parts approve and one deny, exactly one winner on Postgres."""

from __future__ import annotations

import os
import threading
import uuid
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, func, select, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.db import get_db
from app.main import app
from app.models import Base, StaffAction
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
    request_id = created.json()["id"]
    paths = (
        f"/parts-requests/{request_id}/approve",
        f"/parts-requests/{request_id}/deny",
    )
    ticket = {"n": 0}
    lock = threading.Lock()

    def call(_session: object) -> object:
        with lock:
            index = ticket["n"]
            ticket["n"] += 1
        return pg_client.post(paths[index], headers=AUTH)

    results, errors = race(2, call, pg_client.session_factory)
    assert errors == [None, None], errors
    codes = sorted(response.status_code for response in results)
    assert codes == [200, 409], [(response.status_code, response.text) for response in results]
    loser = next(response for response in results if response.status_code == 409)
    assert loser.json()["error"]["code"] == "request_already_decided"
    session = pg_client.session_factory()
    try:
        count = session.scalar(
            select(func.count())
            .select_from(StaffAction)
            .where(StaffAction.request_id == uuid.UUID(request_id))
        )
    finally:
        session.close()
    assert count == 1
