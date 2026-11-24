"""AUD-046 part 1: notify queues pending rows; `python -m app.outbox` sends the batch."""

from __future__ import annotations

import runpy

from fastapi.testclient import TestClient
from sqlalchemy import select

from app.config import Settings
from app.models import NotificationOutbox, NotificationStatus
from app.services import notify
from tests.conftest import AUTH, create_hoist, create_member


class _SMTP:
    """Records each SMTP() so a batch can be checked for one connection."""

    def __init__(self, opened: list) -> None:
        self.opened = opened

    def __call__(self, host, port, timeout=None):
        conn = _Conn()
        self.opened.append(conn)
        return conn


class _Conn:
    def __init__(self) -> None:
        self.sent: list[str] = []
        self.tls = False
        self.user: str | None = None

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        return False

    def starttls(self) -> None:
        self.tls = True

    def login(self, username, password) -> None:
        self.user = username

    def send_message(self, message) -> None:
        self.sent.append(str(message["To"]))


def _smtp_settings() -> Settings:
    return Settings(
        smtp_host="smtp.projectcar.ca",
        smtp_port=587,
        smtp_username="member",
        smtp_password="pw",
        smtp_from="shop@projectcar.ca",
        smtp_use_tls=True,
    )


def test_notify_queues_pending_and_outbox_sends_on_one_connection(client: TestClient, monkeypatch) -> None:
    create_member(client, email="ada@example.com", name="Ada Reyes")
    create_member(client, email="bea@example.com", name="Bea Cole")
    create_hoist(client, name="Bay 1")
    opened: list = []
    settings = _smtp_settings()
    monkeypatch.setattr(notify.smtplib, "SMTP", _SMTP(opened))
    monkeypatch.setattr(notify, "get_settings", lambda: settings)

    response = client.post("/fill/notify", headers=AUTH, json={"dry_run": False, "channels": ["email"]})
    assert response.status_code == 200, response.text
    notes = response.json()["notifications"]
    assert [row["status"] for row in notes] == ["pending", "pending"]
    assert [row["attempts"] for row in notes] == [0, 0]
    assert opened == []

    monkeypatch.setattr("app.db.SessionLocal", client.session_factory)
    monkeypatch.setattr("app.config.get_settings", lambda: settings)
    try:
        runpy.run_module("app.outbox", run_name="__main__")
    except SystemExit as exc:
        assert exc.code == 0
    else:
        raise AssertionError("python -m app.outbox should exit")

    session = client.session_factory()
    try:
        rows = list(session.scalars(select(NotificationOutbox)))
    finally:
        session.close()
    assert len(opened) == 1
    assert opened[0].tls is True
    assert opened[0].user == "member"
    assert sorted(opened[0].sent) == ["ada@example.com", "bea@example.com"]
    assert {row.status for row in rows} == {NotificationStatus.SENT}
    assert {row.attempts for row in rows} == {1}
    assert {row.payload["adapter"] for row in rows} == {"smtp"}


def test_dry_run_and_missing_recipient_are_not_sent(client: TestClient, monkeypatch) -> None:
    create_member(client, email="ada@example.com")
    create_hoist(client, name="Bay 1")
    opened: list = []
    monkeypatch.setattr(notify.smtplib, "SMTP", _SMTP(opened))
    dry = client.post("/fill/notify", headers=AUTH, json={"dry_run": True, "channels": ["email", "sms"]})
    assert dry.status_code == 200, dry.text
    assert {row["status"] for row in dry.json()["notifications"]} == {"dry_run"}
    skipped = client.post("/fill/notify", headers=AUTH, json={"dry_run": False, "channels": ["sms"]})
    assert skipped.status_code == 200, skipped.text
    row = skipped.json()["notifications"][0]
    assert row["status"] == "skipped"
    assert row["last_error"] == "missing_recipient"
    assert row["attempts"] == 0
    assert opened == []
