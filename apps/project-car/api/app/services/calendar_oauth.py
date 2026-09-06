"""Google / Apple calendar connect scaffold. Not two-way sync."""

from __future__ import annotations

from urllib.parse import urlencode

from app.auth import Principal
from app.config import Settings
from app.models import CalendarConnection, CalendarProvider
from sqlalchemy import select
from sqlalchemy.orm import Session

GOOGLE_AUTH = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_SCOPES = "https://www.googleapis.com/auth/calendar.events"


def connection_status(session: Session, principal: Principal, provider: CalendarProvider) -> str:
    stmt = select(CalendarConnection).where(CalendarConnection.provider == provider)
    if principal.role == "owner":
        stmt = stmt.where(
            CalendarConnection.owner_email == principal.email,
            CalendarConnection.member_id.is_(None),
        )
    else:
        stmt = stmt.where(CalendarConnection.member_id == principal.member_id)
    row = session.scalars(stmt).first()
    return row.status if row is not None else "disconnected"


def calendar_payload(session: Session, principal: Principal, settings: Settings) -> dict:
    google_ready = bool(settings.google_oauth_client_id and settings.google_oauth_redirect_uri)
    return {
        "google": {
            "connected": connection_status(session, principal, CalendarProvider.GOOGLE) == "connected",
            "status": connection_status(session, principal, CalendarProvider.GOOGLE),
            "ready": google_ready,
            "label": "Connect Google Calendar",
        },
        "apple": {
            "connected": False,
            "status": "ics_only",
            "ready": True,
            "label": "Add to Apple Calendar",
            "hint": "Download the ICS for a to-do due date. Apple Calendar has no public OAuth in this slice.",
        },
        "next": (
            "Two-way Google Calendar sync needs GOOGLE_OAUTH_CLIENT_ID, "
            "GOOGLE_OAUTH_CLIENT_SECRET, and a registered redirect on ops. "
            "Apple stays ICS import until a CalDAV path is locked."
        ),
    }


def google_authorize_url(settings: Settings, *, state: str) -> str | None:
    if not settings.google_oauth_client_id or not settings.google_oauth_redirect_uri:
        return None
    query = urlencode(
        {
            "client_id": settings.google_oauth_client_id,
            "redirect_uri": settings.google_oauth_redirect_uri,
            "response_type": "code",
            "scope": GOOGLE_SCOPES,
            "access_type": "offline",
            "include_granted_scopes": "true",
            "prompt": "consent",
            "state": state,
        }
    )
    return f"{GOOGLE_AUTH}?{query}"
