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


def _queue(client: TestClient, *, both: bool = True) -> None:
    create_member(client, email="ada@example.com", name="Ada Reyes")
    if both:
        create_member(client, email="bea@example.com", name="Bea Cole")
    create_hoist(client, name="Bay 1")
    response = client.post("/fill/notify", headers=AUTH, json={"dry_run": False, "channels": ["email"]})
    assert response.status_code == 200, response.text


def _mark_failed(client: TestClient, email: str, attempts: int) -> None:
    session = client.session_factory()
    row = session.scalar(select(NotificationOutbox).where(NotificationOutbox.to_address == email))
    assert row is not None
    row.status, row.attempts, row.last_error = NotificationStatus.FAILED, attempts, "smtp_error: down"
    session.commit()
    session.close()


def _send(client: TestClient, monkeypatch, smtp=None) -> list:
    opened: list = []
    settings = Settings(smtp_host="smtp.projectcar.ca", smtp_port=587, smtp_username="member",
                        smtp_password="pw", smtp_use_tls=True)
    monkeypatch.setattr(notify.smtplib, "SMTP", smtp or _SMTP(opened))
    monkeypatch.setattr(notify, "get_settings", lambda: settings)
    monkeypatch.setattr(outbox, "SessionLocal", client.session_factory)
    monkeypatch.setattr(outbox, "get_settings", lambda: settings)
    assert outbox.main() == 0
    return opened


def _by_address(client: TestClient) -> dict[str, NotificationOutbox]:
    session = client.session_factory()
    rows = {row.to_address: row for row in session.scalars(select(NotificationOutbox))}
    session.close()
    return rows


def test_failed_retry_joins_pending_on_one_connection(client: TestClient, monkeypatch) -> None:
    _queue(client)
    _mark_failed(client, "ada@example.com", 1)
    opened = _send(client, monkeypatch)
    rows = _by_address(client)
    assert len(opened) == 1
    assert sorted(opened[0].sent) == ["ada@example.com", "bea@example.com"]
    assert (rows["ada@example.com"].status, rows["ada@example.com"].attempts) == (NotificationStatus.SENT, 2)
    assert (rows["bea@example.com"].status, rows["bea@example.com"].attempts) == (NotificationStatus.SENT, 1)


def test_failed_row_at_attempt_cap_is_not_handed_to_smtp(client: TestClient, monkeypatch) -> None:
    _queue(client)
    _mark_failed(client, "ada@example.com", 5)
    opened = _send(client, monkeypatch)
    row = _by_address(client)["ada@example.com"]
    assert len(opened) == 1 and opened[0].sent == ["bea@example.com"]
    assert row.status == NotificationStatus.FAILED and row.attempts == 5


def test_retry_that_raises_stays_failed_and_increments(client: TestClient, monkeypatch) -> None:
    _queue(client, both=False)
    _mark_failed(client, "ada@example.com", 1)

    class _Boom(_SMTP):
        def send_message(self, message) -> None:
            raise notify.smtplib.SMTPException("mailbox full")

    opened: list = []
    _send(client, monkeypatch, _Boom(opened))
    row = _by_address(client)["ada@example.com"]
    assert len(opened) == 1
    assert row.status == NotificationStatus.FAILED and row.attempts == 2
    assert row.last_error is not None and "mailbox full" in row.last_error
