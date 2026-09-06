"""Durable notification outbox plus channel adapters.

v1 ships a working email path (SMTP when configured, otherwise an in-process
stub that records a send). SMS and push are explicit adapter interfaces so
Twilio / Inbox / web-push can plug in later without rewriting the outbox.
"""

from __future__ import annotations

import smtplib
from dataclasses import dataclass
from email.message import EmailMessage
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.models import (
    FillOffer,
    Member,
    MemberStatus,
    NotificationChannel,
    NotificationOutbox,
    NotificationStatus,
)
from app.services.fill import FillSnapshot, discount_label
from app.shop_time import PRICING_TZ, pricing_now


class NotifyError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass(frozen=True)
class AdapterResult:
    ok: bool
    status: NotificationStatus
    detail: str


class ChannelAdapter(Protocol):
    """Plug-in point for email / SMS / push. Do not call vendors from routers."""

    channel: NotificationChannel

    def deliver(
        self,
        *,
        to_address: str,
        subject: str,
        body: str,
        payload: dict,
    ) -> AdapterResult: ...


class EmailAdapter:
    """SMTP when `SMTP_HOST` is set; otherwise a durable stub that marks sent."""

    channel = NotificationChannel.EMAIL

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    def deliver(
        self,
        *,
        to_address: str,
        subject: str,
        body: str,
        payload: dict,
    ) -> AdapterResult:
        host = (self.settings.smtp_host or "").strip()
        if not host:
            return AdapterResult(
                ok=True,
                status=NotificationStatus.SENT,
                detail="email_stub",
            )
        message = EmailMessage()
        sender = (self.settings.smtp_from or "shop@projectcar.ca").strip()
        message["From"] = sender
        message["To"] = to_address
        message["Subject"] = subject
        message.set_content(body)
        try:
            with smtplib.SMTP(host, self.settings.smtp_port, timeout=15) as smtp:
                if self.settings.smtp_use_tls:
                    smtp.starttls()
                username = (self.settings.smtp_username or "").strip()
                if username:
                    smtp.login(username, self.settings.smtp_password)
                smtp.send_message(message)
        except (OSError, smtplib.SMTPException) as exc:
            return AdapterResult(
                ok=False,
                status=NotificationStatus.FAILED,
                detail=f"smtp_error: {exc}",
            )
        return AdapterResult(ok=True, status=NotificationStatus.SENT, detail="smtp")


class SmsAdapter:
    """Twilio / Inbox SMS is not wired. Interface only."""

    channel = NotificationChannel.SMS

    def deliver(
        self,
        *,
        to_address: str,
        subject: str,
        body: str,
        payload: dict,
    ) -> AdapterResult:
        return AdapterResult(
            ok=False,
            status=NotificationStatus.SKIPPED,
            detail="sms_not_configured",
        )


class PushAdapter:
    """Web-push / Inbox push is not wired. Interface only."""

    channel = NotificationChannel.PUSH

    def deliver(
        self,
        *,
        to_address: str,
        subject: str,
        body: str,
        payload: dict,
    ) -> AdapterResult:
        return AdapterResult(
            ok=False,
            status=NotificationStatus.SKIPPED,
            detail="push_not_configured",
        )


ADAPTERS: dict[NotificationChannel, type[ChannelAdapter]] = {
    NotificationChannel.EMAIL: EmailAdapter,
    NotificationChannel.SMS: SmsAdapter,
    NotificationChannel.PUSH: PushAdapter,
}


def adapter_for(channel: NotificationChannel, settings: Settings | None = None) -> ChannelAdapter:
    cls = ADAPTERS[channel]
    if cls is EmailAdapter:
        return EmailAdapter(settings)
    return cls()


def parse_channels(values: list[str] | None) -> list[NotificationChannel]:
    if not values:
        return [NotificationChannel.EMAIL]
    resolved: list[NotificationChannel] = []
    seen: set[NotificationChannel] = set()
    for raw in values:
        try:
            channel = NotificationChannel(str(raw).strip().lower())
        except ValueError as exc:
            raise NotifyError("invalid_channel", f"Unknown notification channel: {raw}.") from exc
        if channel not in seen:
            seen.add(channel)
            resolved.append(channel)
    if not resolved:
        return [NotificationChannel.EMAIL]
    return resolved


def active_members(session: Session) -> list[Member]:
    rows = session.scalars(
        select(Member).where(Member.status == MemberStatus.ACTIVE).order_by(Member.name)
    ).all()
    return list(rows)


def recipient_for(member: Member, channel: NotificationChannel) -> str | None:
    if channel == NotificationChannel.EMAIL:
        return member.email
    if channel == NotificationChannel.SMS:
        return member.phone
    if channel == NotificationChannel.PUSH:
        return str(member.id)
    return None


def campaign_copy(member: Member, snapshot: FillSnapshot) -> tuple[str, str]:
    date_label = snapshot.target_date.isoformat()
    subject = f"Tomorrow's open hoist hours — {discount_label(snapshot.discount_pct)}% fill discount"
    gap_lines = []
    for gap in snapshot.gaps[:12]:
        local_start = gap.start_at.astimezone(PRICING_TZ).strftime("%H:%M")
        local_end = gap.end_at.astimezone(PRICING_TZ).strftime("%H:%M")
        gap_lines.append(f"- {gap.hoist_name}: {local_start}–{local_end} ({gap.hours}h)")
    gaps_block = "\n".join(gap_lines) if gap_lines else "- (see Shop OS schedule)"
    body = (
        f"Hi {member.name},\n\n"
        f"Customer bays have open hours tomorrow ({date_label}, America/Regina).\n"
        f"Fill discount: {discount_label(snapshot.discount_pct)}% on next-day open slots "
        f"({snapshot.open_hours} open of {snapshot.capacity_hours} bay-hours; "
        f"urgency {snapshot.urgency}).\n\n"
        f"Openings:\n{gaps_block}\n\n"
        "This is a Shop OS member notice — not a public price. The shop is not "
        "open. Tokens only. No Stripe.\n"
    )
    return subject, body


def enqueue_fill_campaign(
    session: Session,
    snapshot: FillSnapshot,
    *,
    channels: list[NotificationChannel],
    dry_run: bool,
    offer: FillOffer | None,
    settings: Settings | None = None,
) -> list[NotificationOutbox]:
    if not snapshot.applies:
        raise NotifyError("no_openings", "No next-day customer-bay openings to notify about.")
    members = active_members(session)
    if not members:
        raise NotifyError("no_members", "No active members to notify.")
    cfg = settings or get_settings()
    rows: list[NotificationOutbox] = []
    for member in members:
        subject, body = campaign_copy(member, snapshot)
        payload = {
            "kind": "fill_gaps",
            "target_date": snapshot.target_date.isoformat(),
            "discount_pct": str(snapshot.discount_pct),
            "fill_multiplier": str(snapshot.fill_multiplier),
            "open_hours": str(snapshot.open_hours),
            "capacity_hours": str(snapshot.capacity_hours),
            "urgency": snapshot.urgency,
            "dry_run": dry_run,
            "member_id": str(member.id),
        }
        for channel in channels:
            to_address = recipient_for(member, channel)
            row = NotificationOutbox(
                channel=channel,
                member_id=member.id,
                to_address=to_address,
                subject=subject,
                body=body,
                payload=payload,
                status=NotificationStatus.DRY_RUN if dry_run else NotificationStatus.PENDING,
                dry_run=dry_run,
                fill_offer_id=offer.id if offer is not None else None,
            )
            if not dry_run and not to_address:
                row.status = NotificationStatus.SKIPPED
                row.last_error = "missing_recipient"
            session.add(row)
            rows.append(row)
    session.flush()
    if not dry_run:
        for row in rows:
            if row.status != NotificationStatus.PENDING:
                continue
            _deliver_row(session, row, settings=cfg)
    return rows


def _deliver_row(
    session: Session,
    row: NotificationOutbox,
    *,
    settings: Settings | None = None,
) -> NotificationOutbox:
    adapter = adapter_for(row.channel, settings)
    result = adapter.deliver(
        to_address=row.to_address or "",
        subject=row.subject or "",
        body=row.body or "",
        payload=row.payload or {},
    )
    row.attempts = int(row.attempts or 0) + 1
    row.status = result.status
    row.last_error = None if result.ok else result.detail
    if result.status == NotificationStatus.SENT:
        row.sent_at = pricing_now()
        extra = dict(row.payload or {})
        extra["adapter"] = result.detail
        row.payload = extra
    elif result.status == NotificationStatus.SKIPPED:
        row.last_error = result.detail
    session.add(row)
    session.flush()
    return row


def list_outbox(session: Session, *, limit: int = 50) -> list[NotificationOutbox]:
    rows = session.scalars(
        select(NotificationOutbox).order_by(NotificationOutbox.created_at.desc()).limit(limit)
    ).all()
    return list(rows)
