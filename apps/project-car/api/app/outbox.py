"""Deliver pending and retryable failed rows on one SMTP connection. ``python -m app.outbox``."""

from __future__ import annotations

from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.db import SessionLocal
from app.models import NotificationChannel, NotificationOutbox, NotificationStatus
from app.services import notify

# Stand-in cap until Ben sets a real limit. The caller's 5-minute interval is the backoff step.
_RETRY_CAP = 5


def deliver_pending(session: Session, settings: Settings | None = None) -> int:
    cfg = settings or get_settings()
    due = or_(
        NotificationOutbox.status == NotificationStatus.PENDING,
        and_(
            NotificationOutbox.status == NotificationStatus.FAILED,
            NotificationOutbox.channel == NotificationChannel.EMAIL,
            NotificationOutbox.attempts < _RETRY_CAP,
        ),
    )
    rows = list(session.scalars(
        select(NotificationOutbox).where(due).order_by(NotificationOutbox.created_at)))
    host = (cfg.smtp_host or "").strip()
    batch = [row for row in rows if row.channel == NotificationChannel.EMAIL and host]
    for row in rows:
        if row.channel != NotificationChannel.EMAIL or not host:
            notify._deliver_row(session, row, settings=cfg)
    if not batch:
        return len(rows)
    untouched = {row.id for row in batch}
    try:
        with notify.smtplib.SMTP(host, cfg.smtp_port, timeout=15) as smtp:
            if cfg.smtp_use_tls:
                smtp.starttls()
            username = (cfg.smtp_username or "").strip()
            if username:
                smtp.login(username, cfg.smtp_password)
            for row in batch:
                notify._deliver_row(session, row, settings=cfg, smtp=smtp)
                untouched.discard(row.id)
    except (OSError, notify.smtplib.SMTPException) as exc:
        detail = f"smtp_error: {exc}"[:500]
        for row in batch:
            if row.id in untouched:
                row.attempts = int(row.attempts or 0) + 1
                row.status, row.last_error = NotificationStatus.FAILED, detail
        session.flush()
    return len(rows)


def main() -> int:
    session = SessionLocal()
    try:
        count = deliver_pending(session)
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
    print(f"outbox delivered {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
