"""Lock in get_db commit before http.response.start (PC-AUD-002)."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.orm import Session

from app.config import get_settings
from app.deps import current_settings
from app.main import app
from tests.conftest import AUTH


def _payload(email: str) -> dict:
    return {
        "name": "Pat Kim",
        "email": email,
        "phone": "555-0102",
        "notes": "aud-002",
    }


def _transport(client: TestClient):
    transport = getattr(client, "_transport", None)
    if transport is None:
        transport = client.transport
    return transport


@contextmanager
def _waitlist_enabled() -> Iterator[None]:
    current = get_settings()
    try:
        if hasattr(current, "model_copy"):
            enabled = current.model_copy(update={"pc_waitlist": True})
        else:
            enabled = current.copy(update={"pc_waitlist": True})
    except Exception:
        object.__setattr__(current, "pc_waitlist", True)
        enabled = current
    previous = app.dependency_overrides.get(current_settings)
    app.dependency_overrides[current_settings] = lambda: enabled
    try:
        yield
    finally:
        if previous is None:
            app.dependency_overrides.pop(current_settings, None)
        else:
            app.dependency_overrides[current_settings] = previous


@contextmanager
def _spy(client: TestClient, host: str) -> Iterator[list[str]]:
    """Record after_commit, then the ASGI response start. Restore the client IP."""
    order: list[str] = []
    transport = _transport(client)
    previous_app = transport.app
    previous_client = transport.client

    def on_commit(_session: Session) -> None:
        order.append("commit")

    async def wrapped(scope, receive, send):
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                order.append("http.response.start:" + str(message["status"]))
            await send(message)

        await previous_app(scope, receive, send_wrapper)

    event.listen(Session, "after_commit", on_commit)
    transport.app = wrapped
    transport.client = (host, 50000)
    try:
        yield order
    finally:
        event.remove(Session, "after_commit", on_commit)
        transport.app = previous_app
        transport.client = previous_client


def test_commit_happens_before_response_start(client: TestClient) -> None:
    with _waitlist_enabled(), _spy(client, "203.0.113.102") as order:
        response = client.post(
            "/waitlist",
            json=_payload("pat.aud002@example.com"),
            headers=AUTH,
        )
    assert response.status_code == 201, response.text
    assert order == ["commit", "http.response.start:201"], order


def test_commit_failure_is_reported(client: TestClient) -> None:
    def fail_commit(_session: Session) -> None:
        raise RuntimeError("forced commit failure")

    transport = _transport(client)
    previous_client = transport.client
    previous_raise = transport.raise_server_exceptions
    event.listen(Session, "before_commit", fail_commit)
    transport.client = ("203.0.113.103", 50000)
    transport.raise_server_exceptions = False
    try:
        with _waitlist_enabled():
            response = client.post(
                "/waitlist",
                json=_payload("pat.aud002.fail@example.com"),
                headers=AUTH,
            )
    finally:
        event.remove(Session, "before_commit", fail_commit)
        transport.client = previous_client
        transport.raise_server_exceptions = previous_raise
    assert response.status_code == 500, response.text
