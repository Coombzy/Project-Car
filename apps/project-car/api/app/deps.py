from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import Cookie, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.auth import (
    Principal,
    bearer_matches,
    read_member_session_token,
    read_session_token,
)
from app.config import Settings, get_settings
from app.db import get_db
from app.models import Member, MemberStatus


def current_settings() -> Settings:
    return get_settings()


def _unauthorized(message: str = "Owner authentication required.") -> HTTPException:
    return HTTPException(
        status_code=401,
        detail={"code": "unauthorized", "message": message},
    )


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

    raise _unauthorized()


def require_member(
    settings: Annotated[Settings, Depends(current_settings)],
    session: Annotated[Session, Depends(get_db)],
    member_session_cookie: Annotated[str | None, Cookie(alias="pc_member_session")] = None,
) -> Principal:
    """Member session cookie. Parallel to Owner. Not OIDC — Staff OIDC can follow."""
    payload = (
        read_member_session_token(settings, member_session_cookie) if member_session_cookie else None
    )
    if not payload:
        raise _unauthorized("Member authentication required.")

    try:
        member_id = UUID(str(payload.get("member_id")))
    except (TypeError, ValueError):
        raise _unauthorized("Member authentication required.") from None

    member = session.get(Member, member_id)
    if member is None:
        raise _unauthorized("Member authentication required.")
    if member.status != MemberStatus.ACTIVE:
        raise HTTPException(
            status_code=403,
            detail={"code": "member_not_bookable", "message": "Only active members can use self-serve."},
        )
    return Principal(role="member", email=member.email, member_id=member.id)


def require_principal(
    settings: Annotated[Settings, Depends(current_settings)],
    session: Annotated[Session, Depends(get_db)],
    authorization: Annotated[str | None, Header()] = None,
    session_cookie: Annotated[str | None, Cookie(alias="pc_owner_session")] = None,
    member_session_cookie: Annotated[str | None, Cookie(alias="pc_member_session")] = None,
) -> Principal:
    """Owner cookie/bearer or Member cookie. Used by GET /me."""
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1].strip()
        if bearer_matches(settings, token):
            return Principal(role="owner", email=settings.owner_email)

    owner_payload = read_session_token(settings, session_cookie) if session_cookie else None
    if owner_payload:
        return Principal(role="owner", email=str(owner_payload.get("email") or settings.owner_email))

    member_payload = (
        read_member_session_token(settings, member_session_cookie) if member_session_cookie else None
    )
    if member_payload:
        try:
            member_id = UUID(str(member_payload.get("member_id")))
        except (TypeError, ValueError):
            raise _unauthorized("Authentication required.") from None
        member = session.get(Member, member_id)
        if member is None or member.status != MemberStatus.ACTIVE:
            raise _unauthorized("Authentication required.")
        return Principal(role="member", email=member.email, member_id=member.id)

    raise _unauthorized("Authentication required.")


DbSession = Annotated[Session, Depends(get_db)]
Owner = Annotated[Principal, Depends(require_owner)]
MemberUser = Annotated[Principal, Depends(require_member)]
AnyPrincipal = Annotated[Principal, Depends(require_principal)]
AppSettings = Annotated[Settings, Depends(current_settings)]
