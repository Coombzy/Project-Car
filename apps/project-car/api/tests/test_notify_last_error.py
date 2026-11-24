"""AUD-008: SMTP failures store at most 500 characters in last_error."""

import smtplib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import Settings
from app.models import Base, NotificationChannel, NotificationOutbox, NotificationStatus
from app.services import notify

_SMTP_ERROR = "x" * 600


class _RaisingSMTP:
    def __call__(self, host, port, timeout=None):
        raise smtplib.SMTPException(_SMTP_ERROR)


def test_smtp_error_last_error_is_clipped_to_500(monkeypatch):
    monkeypatch.setattr(notify.smtplib, "SMTP", _RaisingSMTP())
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)()
    row = NotificationOutbox(
        channel=NotificationChannel.EMAIL,
        to_address="rider@projectcar.ca",
        subject="Fill notice",
        body="Open bays tomorrow.",
        status=NotificationStatus.PENDING,
    )
    session.add(row)
    session.flush()
    delivered = notify._deliver_row(
        session,
        row,
        settings=Settings(smtp_host="smtp.projectcar.ca", smtp_port=587, smtp_use_tls=False),
    )
    session.flush()
    assert delivered.status is NotificationStatus.FAILED
    assert delivered.last_error == f"smtp_error: {_SMTP_ERROR}"[:500]
    assert len(delivered.last_error) == 500
    session.close()
