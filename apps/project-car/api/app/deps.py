from __future__ import annotations

from typing import Annotated

from fastapi import Cookie, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.auth import Principal, bearer_matches, read_session_token
from app.config import Settings, get_settings
from app.db import get_db


def current_settings() -> Settings:
    return get_settings()


def require_owner(
    settings: Annotated[Settings, Depends(current_settings)],
    authorization: Annotated[str | None, Header()] = None,
    session_cookie: Annotated[str | None, Cookie(alias="pc_owner_session")] = None,
) -> Principal:
    """v1 Owner stub: httpOnly session cookie or Bearer OWNER_API_SECRET."""
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1].strip()
        if bearer_matches(settings, token):
            return Principal(role="owner", email=settings.owner_email)

    payload = read_session_token(settings, session_cookie) if session_cookie else None
    if payload:
        return Principal(role="owner", email=str(payload.get("email") or settings.owner_email))

    raise HTTPException(
        status_code=401,
        detail={"code": "unauthorized", "message": "Owner authentication required."},
    )


DbSession = Annotated[Session, Depends(get_db)]
Owner = Annotated[Principal, Depends(require_owner)]
AppSettings = Annotated[Settings, Depends(current_settings)]
