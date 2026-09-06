from __future__ import annotations

from fastapi import APIRouter, HTTPException
from itsdangerous import URLSafeTimedSerializer

from app.deps import AnyPrincipal, AppSettings, DbSession
from app.schemas import CalendarStatusOut
from app.services.calendar_oauth import calendar_payload, google_authorize_url

router = APIRouter(tags=["calendar"])


def _error(status: int, code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status, detail={"code": code, "message": message})


@router.get("/calendar/status", response_model=CalendarStatusOut)
def calendar_status(session: DbSession, principal: AnyPrincipal, settings: AppSettings) -> CalendarStatusOut:
    return CalendarStatusOut.model_validate(calendar_payload(session, principal, settings))


@router.get("/calendar/google/start")
def google_start(principal: AnyPrincipal, settings: AppSettings) -> dict:
    """Scaffold only. Returns authorize URL when env is set; otherwise 501."""
    serializer = URLSafeTimedSerializer(settings.session_secret, salt="project-car-google-cal")
    state = serializer.dumps({"role": principal.role, "email": principal.email})
    url = google_authorize_url(settings, state=state)
    if url is None:
        raise _error(
            501,
            "calendar_oauth_not_configured",
            "Google Calendar OAuth is not configured. Set GOOGLE_OAUTH_CLIENT_ID and "
            "GOOGLE_OAUTH_REDIRECT_URI, or download an ICS from a to-do.",
        )
    return {"authorize_url": url, "configured": True}


@router.get("/calendar/google/callback")
def google_callback() -> dict:
    raise _error(
        501,
        "calendar_oauth_not_complete",
        "Google token exchange is scaffolded, not production-complete. Use ICS export for now.",
    )


@router.get("/calendar/apple/start")
def apple_start() -> dict:
    raise _error(
        501,
        "apple_calendar_ics_only",
        "Apple Calendar has no OAuth in this slice. Download a to-do ICS and import it.",
    )
