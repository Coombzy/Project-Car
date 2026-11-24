"""AUD-046 part 1: notify queues pending rows; python -m app.outbox sends them."""

from fastapi.testclient import TestClient
from sqlalchemy import select

from app import outbox
from app.config import Settings
from app.models import NotificationOutbox, NotificationStatus
from app.services import notify
from tests.conftest import AUTH, create_hoist, create_member


class _SMTP:
    def __init__(self, opened: list) -> None:
        self.opened = opened

    def __call__(self, host, port, timeout=None):
        self.sent: list[str] = []
        self.opened.append(self)
        return self

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


def test_notify_queues_pending_and_sender_uses_one_connection(client: TestClient, monkeypatch) -> None:
    create_member(client, email="ada@example.com", name="Ada Reyes")
    create_member(client, email="bea@example.com", name="Bea Cole")
    create_hoist(client, name="Bay 1")
    opened: list = []
    settings = Settings(smtp_host="smtp.projectcar.ca", smtp_port=587, smtp_username="member",
                        smtp_password="pw", smtp_use_tls=True)
    monkeypatch.setattr(notify.smtplib, "SMTP", _SMTP(opened))
    monkeypatch.setattr(notify, "get_settings", lambda: settings)
    response = client.post("/fill/notify", headers=AUTH, json={"dry_run": False, "channels": ["email"]})
    assert response.status_code == 200, response.text
    notes = response.json()["notifications"]
    assert [row["status"] for row in notes] == ["pending", "pending"]
    assert [row["attempts"] for row in notes] == [0, 0]
    assert opened == []

    monkeypatch.setattr(outbox, "SessionLocal", client.session_factory)
    monkeypatch.setattr(outbox, "get_settings", lambda: settings)
    assert outbox.main() == 0
    session = client.session_factory()
    rows = list(session.scalars(select(NotificationOutbox)))
    session.close()
    assert len(opened) == 1
    assert opened[0].tls is True and opened[0].user == "member"
    assert sorted(opened[0].sent) == ["ada@example.com", "bea@example.com"]
    assert {row.status for row in rows} == {NotificationStatus.SENT}
    assert {row.attempts for row in rows} == {1}
    assert {(row.payload or {})["adapter"] for row in rows} == {"smtp"}
