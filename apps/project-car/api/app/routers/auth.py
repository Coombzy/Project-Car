from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request, Response
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.auth import (
    DUMMY_MEMBER_PASSWORD_HASH,
    clear_member_session_cookie,
    clear_session_cookie,
    create_member_session_token,
    create_session_token,
    credentials_match,
    login_failure_limited,
    member_password_matches,
    rate_limited_error,
    record_login_failure,
    reject_dev_secret,
    set_member_session_cookie,
    set_session_cookie,
    verify_password,
)
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
    client = request.client
    if client is None or not client.host:
        return "unknown"
    return client.host


def _guard_login(request: Request, settings: AppSettings) -> str:
    """Refuse a dev session secret, then apply the in-process IP lockout."""
    reject_dev_secret(settings.session_secret)
    client_ip = _client_ip(request)
    if login_failure_limited(client_ip):
        raise rate_limited_error()
    return client_ip


@router.post("/auth/login", response_model=PrincipalOut)
def login(
    body: LoginRequest,
    request: Request,
    response: Response,
    settings: AppSettings,
) -> PrincipalOut:
    client_ip = _guard_login(request, settings)
    if not credentials_match(settings, body.email, body.password):
        record_login_failure(client_ip)
        raise _invalid_credentials()
    token = create_session_token(settings, body.email)
    set_session_cookie(response, settings, token)
    return PrincipalOut(role="owner", email=body.email)


@router.post("/auth/logout", response_model=PrincipalOut)
def logout(response: Response, settings: AppSettings) -> PrincipalOut:
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
    refused for that member. A member with no hash yet still accepts the shared
    demo password, so existing rows keep working until an owner sets one.

    Unknown emails and members who are not active both return invalid
    credentials. The body does not say which case it was.

    Not OIDC. Staff / Member OIDC can replace this later without rewriting shop tables.
    """
    client_ip = _guard_login(request, settings)
    member = session.scalars(
        select(Member).options(selectinload(Member.tier)).where(Member.email == str(body.email))
    ).first()
    if member is None:
        verify_password(body.password, DUMMY_MEMBER_PASSWORD_HASH)
        record_login_failure(client_ip)
        raise _invalid_credentials()
    if not member_password_matches(
        member.password_hash, body.password, settings.member_demo_password
    ):
        record_login_failure(client_ip)
        raise _invalid_credentials()
    if member.status != MemberStatus.ACTIVE:
        record_login_failure(client_ip)
        raise _invalid_credentials()
    token = create_member_session_token(settings, member.email, member.id)
    set_member_session_cookie(response, settings, token)
    return PrincipalOut(role="member", email=member.email, member_id=member.id)


@router.post("/auth/member/logout", response_model=PrincipalOut)
def member_logout(response: Response, settings: AppSettings) -> PrincipalOut:
    clear_member_session_cookie(response, settings)
    return PrincipalOut(role="anonymous", email="")


@router.get("/me", response_model=PrincipalOut)
def me(principal: AnyPrincipal) -> PrincipalOut:
    return PrincipalOut(role=principal.role, email=principal.email, member_id=principal.member_id)
