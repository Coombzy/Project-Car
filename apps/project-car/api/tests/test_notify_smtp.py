"""Real SMTP delivery path of notify.EmailAdapter.deliver (notify.py:84-104), with a fake smtplib.SMTP."""

import smtplib
from email.message import EmailMessage

import pytest

from app.config import Settings
from app.models import NotificationStatus
from app.services import notify


class FakeSMTP:
    """Stand-in for smtplib.SMTP that records every call it receives."""

    def __init__(self, calls, error=None):
        self.calls = calls
        self.error = error

    def __call__(self, host, port, timeout=None):
        self.calls.append(("connect", host, port, timeout))
        if self.error is not None:
            raise self.error
        return self

    def __enter__(self):
        self.calls.append(("enter",))
        return self

    def __exit__(self, *exc_info):
        self.calls.append(("close",))
        return False

    def starttls(self):
        self.calls.append(("starttls",))

    def login(self, username, password):
        self.calls.append(("login", username, password))

    def send_message(self, message):
        self.calls.append(("send_message", message))


def make_settings(**overrides):
    base = dict(smtp_host="smtp.projectcar.ca", smtp_port=587, smtp_username="member",
                smtp_password="pw", smtp_from="Shop <shop@projectcar.ca>", smtp_use_tls=True)
    base.update(overrides)
    return Settings(**base)


def deliver(adapter):
    return adapter.deliver(
        to_address="rider@projectcar.ca",
        subject="Fill notice",
        body="Open bays tomorrow.",
        payload={"kind": "fill_gaps"},
    )


@pytest.fixture
def calls(monkeypatch):
    recorded: list[tuple] = []
    monkeypatch.setattr(notify.smtplib, "SMTP", FakeSMTP(recorded))
    return recorded


def test_real_smtp_path_sends_message(calls):
    result = deliver(notify.EmailAdapter(make_settings()))
    assert result.ok is True
    assert result.status is NotificationStatus.SENT
    assert result.detail == "smtp"
    assert calls[0] == ("connect", "smtp.projectcar.ca", 587, 15)
    assert [c[0] for c in calls] == ["connect", "enter", "starttls", "login", "send_message", "close"]
    message = calls[4][1]
    assert isinstance(message, EmailMessage)
    assert message["From"] == "Shop <shop@projectcar.ca>"
    assert message["To"] == "rider@projectcar.ca"
    assert message["Subject"] == "Fill notice"
    assert "Open bays tomorrow." in message.get_content()


def test_tls_and_login_are_optional(calls):
    adapter = notify.EmailAdapter(make_settings(smtp_use_tls=False, smtp_username="   "))
    result = deliver(adapter)
    assert result.ok is True
    assert result.detail == "smtp"
    assert [c[0] for c in calls] == ["connect", "enter", "send_message", "close"]


@pytest.mark.parametrize(
    "error", [smtplib.SMTPServerDisconnected("no server"), OSError("connection refused")]
)
def test_smtp_failure_returns_failed_result(monkeypatch, error):
    recorded: list[tuple] = []
    monkeypatch.setattr(notify.smtplib, "SMTP", FakeSMTP(recorded, error=error))
    result = deliver(notify.EmailAdapter(make_settings()))
    assert result.ok is False
    assert result.status is NotificationStatus.FAILED
    assert result.detail.startswith("smtp_error:")
    assert str(error) in result.detail


def test_mutant_skipping_smtp_path_is_detected(calls):
    # A mutant that returns the stub path never constructs smtplib.SMTP or sends.
    result = deliver(notify.EmailAdapter(make_settings()))
    assert result.detail != "email_stub"
    assert calls[0] == ("connect", "smtp.projectcar.ca", 587, 15)
    assert calls[-2][0] == "send_message"
    assert calls[-1] == ("close",)


def test_empty_host_stays_on_stub_path(calls):
    result = deliver(notify.EmailAdapter(make_settings(smtp_host="   ")))
    assert result.ok is True
    assert result.detail == "email_stub"
    assert calls == []
