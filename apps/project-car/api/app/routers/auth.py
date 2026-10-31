from __future__ import annotations

from fastapi import APIRouter, Cookie, HTTPException, Request, Response
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.auth import (
    DUMMY_MEMBER_PASSWORD_HASH,
    bump_owner_epoch,
    clear_member_session_cookie,
    clear_session_cookie,
    create_member_session_token,
    create_session_token,
    credentials_match,
    current_owner_epoch,
    member_password_matches,
    owner_session_current,
    rate_limited_error,
    read_session_token,
    release_login_failure,
    reserve_login_failure,
    reject_dev_secret,
    set_member_session_cookie,
    set_session_cookie,
    verify_password,
)
from app.client_ip import client_ip
from app.config import get_settings
from app.deps import AnyPrincipal, AppSettings, DbSession
from app.models import Member, MemberStatus
from app.schemas import LoginRequest, PrincipalOut

router = APIRouter(tags=["auth"])


def _invalid_credentials() -> HTTPException:
    return HTTPException(
        status_code=401,
        detail={"code": "invalid_credentials", "message": "Email or password is incorrect."},
    )


def _client_ip(request: Request) -> str:
    return client_ip(request, get_settings().client_ip_header)


def _guard_login(
    request: Request, settings: AppSettings, *, realm: str, account: str
) -> tuple[str, object]:
    """Refuse a dev session secret, then reserve one in-process failure slot."""
    reject_dev_secret(settings.session_secret)
    address = _client_ip(request)
    stamp = reserve_login_failure(address, realm=realm, account=account)
    if stamp is None:
        raise rate_limited_error()
    return address, stamp


@router.post("/auth/login", response_model=PrincipalOut)
def login(
    body: LoginRequest,
    request: Request,
    response: Response,
    settings: AppSettings,
    session: DbSession,
) -> PrincipalOut:
    address, stamp = _guard_login(request, settings, realm="owner", account=str(body.email))
    if not credentials_match(settings, body.email, body.password):
        raise _invalid_credentials()
    token = create_session_token(settings, body.email, epoch=current_owner_epoch(session))
    set_session_cookie(response, settings, token)
    release_login_failure(address, stamp)
    return PrincipalOut(role="owner", email=body.email)


@router.post("/auth/logout", response_model=PrincipalOut)
def logout(
    response: Response,
    settings: AppSettings,
    session: DbSession,
    session_cookie: str | None = Cookie(default=None, alias="pc_owner_session"),
) -> PrincipalOut:
    """Clear this browser's cookie and revoke every owner session."""
    if session_cookie:
        payload = read_session_token(settings, session_cookie)
        if payload is not None and owner_session_current(settings, session, payload):
            bump_owner_epoch(session)
    clear_session_cookie(response, settings)
    return PrincipalOut(role="anonymous", email="")


@router.post("/auth/member/login", response_model=PrincipalOut)
def member_login(
    body: LoginRequest,
    request: Request,
    response: Response,
    settings: AppSettings,
    session: DbSession,
) -> PrincipalOut:
    """Member session. Email must match a member row.

    A stored password hash is checked on its own. The shared demo password is
    refused for that member. A member with no hash accepts the shared demo
    password on loopback, and off loopback only when that password is not the
    default. Off loopback the default is the same 401 as a wrong password.

    Unknown emails and members who are not active both return invalid
    credentials. The body does not say which case it was.

    The session payload includes a short fingerprint of the current password
    hash, or ``none`` when the member has no hash. It is not the hash.

    Not OIDC. Staff / Member OIDC can replace this later without rewriting shop tables.
    """
    address, stamp = _guard_login(
        request, settings, realm="member", account=str(body.email)
    )
    member = session.scalars(
        select(Member).options(selectinload(Member.tier)).where(Member.email == str(body.email))
    ).first()
    if member is None:
        verify_password(body.password, DUMMY_MEMBER_PASSWORD_HASH)
        raise _invalid_credentials()
    if not member_password_matches(
        member.password_hash, body.password, settings.member_demo_password
    ):
        raise _invalid_credentials()
    if member.status != MemberStatus.ACTIVE:
        raise _invalid_credentials()
    token = create_member_session_token(settings, member.email, member.id, member.password_hash)
    set_member_session_cookie(response, settings, token)
    release_login_failure(address, stamp)
    return PrincipalOut(role="member", email=member.email, member_id=member.id)


@router.post("/auth/member/logout", response_model=PrincipalOut)
def member_logout(response: Response, settings: AppSettings) -> PrincipalOut:
    clear_member_session_cookie(response, settings)
    return PrincipalOut(role="anonymous", email="")


@router.get("/me", response_model=PrincipalOut)
def me(principal: AnyPrincipal) -> PrincipalOut:
    return PrincipalOut(role=principal.role, email=principal.email, member_id=principal.member_id)
