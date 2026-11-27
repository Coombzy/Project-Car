from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import Depends, Header, HTTPException, Request
from sqlalchemy.orm import Session

from app.auth import (
    Principal,
    ai_bearer_matches,
    bearer_matches,
    member_password_fingerprint_matches,
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
    email = payload.get("email")
    if not isinstance(email, str) or not email or email != settings.owner_email:
        return None
    return Principal(role="owner", email=settings.owner_email)


# AUD-009 part 1. These three writes only; not the R101 allowlist.
_AI_REFUSALS: dict[str, tuple[str, str]] = {
    "/members/{member_id}/password": (
        "ai_cannot_set_password",
        "An AI cannot set a member's password on its own.",
    ),
    "/members": ("ai_not_allowed", "An AI cannot create a member on its own."),
    "/waitlist/{entry_id}/convert": (
        "ai_not_allowed",
        "An AI cannot convert a waitlist row on its own.",
    ),
}


def _owner_route_path(request: Request) -> str:
    route = request.scope.get("route")
    template = getattr(route, "path", None)
    if isinstance(template, str):
        return template
    parts = [part for part in request.url.path.split("/") if part]
    if len(parts) == 3 and parts[0] == "members" and parts[2] == "password":
        return "/members/{member_id}/password"
    if len(parts) == 3 and parts[0] == "waitlist" and parts[2] == "convert":
        return "/waitlist/{entry_id}/convert"
    return request.url.path


def _refuse_ai_owner_route(request: Request) -> None:
    if request.method != "POST":
        return
    refusal = _AI_REFUSALS.get(_owner_route_path(request))
    if refusal is None:
        return
    code, message = refusal
    raise HTTPException(status_code=403, detail={"code": code, "message": message})


def require_owner(
    request: Request,
    settings: Annotated[Settings, Depends(current_settings)],
    authorization: Annotated[str | None, Header()] = None,
) -> Principal:
    """Staff stub: human Owner cookie/bearer, or the same routes with the AI bearer."""
    session_cookie = request.cookies.get(settings.cookie_name)
    bearer = _bearer_principal(settings, authorization)
    if bearer is not None:
        if bearer.role == "ai":
            _refuse_ai_owner_route(request)
        return bearer
    owner = _owner_from_cookie(settings, session_cookie)
    if owner is not None:
        return owner
    raise _unauthorized()


# scope="function": get_db commits before the response is sent (PC-AUD-002).
DbSession = Annotated[Session, Depends(get_db, scope="function")]

def require_member(
    request: Request,
    settings: Annotated[Settings, Depends(current_settings)],
    session: DbSession,
) -> Principal:
    """Member session cookie. Parallel to Owner. Not OIDC — Staff OIDC can follow."""
    member_session_cookie = request.cookies.get(settings.member_cookie_name)
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
    if not member_password_fingerprint_matches(
        settings, payload.get("pwd_fp"), member.password_hash
    ):
        raise _unauthorized("Member authentication required.")
    if member.status != MemberStatus.ACTIVE:
        raise HTTPException(
            status_code=403,
            detail={"code": "member_not_bookable", "message": "Only active members can use self-serve."},
        )
    return Principal(role="member", email=member.email, member_id=member.id)


def require_principal(
    request: Request,
    settings: Annotated[Settings, Depends(current_settings)],
    session: DbSession,
    authorization: Annotated[str | None, Header()] = None,
) -> Principal:
    """Owner cookie/bearer or Member cookie. Used by GET /me."""
    session_cookie = request.cookies.get(settings.cookie_name)
    member_session_cookie = request.cookies.get(settings.member_cookie_name)
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
        if not member_password_fingerprint_matches(
            settings, member_payload.get("pwd_fp"), member.password_hash
        ):
            raise _unauthorized("Authentication required.")
        return Principal(role="member", email=member.email, member_id=member.id)

    raise _unauthorized("Authentication required.")


Owner = Annotated[Principal, Depends(require_owner)]
MemberUser = Annotated[Principal, Depends(require_member)]
AnyPrincipal = Annotated[Principal, Depends(require_principal)]
AppSettings = Annotated[Settings, Depends(current_settings)]
