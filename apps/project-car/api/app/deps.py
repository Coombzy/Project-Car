from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import Cookie, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.auth import (
    Principal,
    ai_bearer_matches,
    bearer_matches,
    read_member_session_token,
    read_session_token,
    reject_dev_secret,
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


def _bearer_principal(settings: Settings, authorization: str | None) -> Principal | None:
    if not authorization or not authorization.lower().startswith("bearer "):
        return None
    token = authorization.split(" ", 1)[1].strip()
    if ai_bearer_matches(settings, token):
        reject_dev_secret(settings.ai_api_secret)
        return Principal(role="ai", email=settings.ai_actor_id)
    if bearer_matches(settings, token):
        reject_dev_secret(settings.owner_api_secret)
        return Principal(role="owner", email=settings.owner_email)
    return None


def _owner_from_cookie(settings: Settings, session_cookie: str | None) -> Principal | None:
    if not session_cookie:
        return None
    payload = read_session_token(settings, session_cookie)
    if not payload:
        return None
    reject_dev_secret(settings.session_secret)
    return Principal(role="owner", email=str(payload.get("email") or settings.owner_email))


def require_owner(
    settings: Annotated[Settings, Depends(current_settings)],
    authorization: Annotated[str | None, Header()] = None,
    session_cookie: Annotated[str | None, Cookie(alias="pc_owner_session")] = None,
) -> Principal:
    """Staff stub: human Owner cookie/bearer, or the same routes with the AI bearer."""
    bearer = _bearer_principal(settings, authorization)
    if bearer is not None:
        return bearer
    owner = _owner_from_cookie(settings, session_cookie)
    if owner is not None:
        return owner
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
    reject_dev_secret(settings.session_secret)

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
    bearer = _bearer_principal(settings, authorization)
    if bearer is not None:
        return bearer

    owner = _owner_from_cookie(settings, session_cookie)
    if owner is not None:
        return owner

    member_payload = (
        read_member_session_token(settings, member_session_cookie) if member_session_cookie else None
    )
    if member_payload:
        reject_dev_secret(settings.session_secret)
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
