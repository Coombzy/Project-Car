from __future__ import annotations

from fastapi import APIRouter, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.auth import (
    DUMMY_MEMBER_PASSWORD_HASH,
    clear_member_session_cookie,
    clear_session_cookie,
    create_member_session_token,
    create_session_token,
    credentials_match,
    member_password_matches,
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


@router.post("/auth/login", response_model=PrincipalOut)
def login(body: LoginRequest, response: Response, settings: AppSettings) -> PrincipalOut:
    if not credentials_match(settings, body.email, body.password):
        raise HTTPException(
            status_code=401,
            detail={"code": "invalid_credentials", "message": "Email or password is incorrect."},
        )
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
    response: Response,
    settings: AppSettings,
    session: DbSession,
) -> PrincipalOut:
    """Member session. Email must match a member row.

    A stored password hash is checked on its own. The shared demo password is
    refused for that member. A member with no hash yet still accepts the shared
    demo password, so existing rows keep working until an owner sets one.

    Not OIDC. Staff / Member OIDC can replace this later without rewriting shop tables.
    """
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
        raise HTTPException(
            status_code=403,
            detail={"code": "member_not_bookable", "message": "Only active members can sign in."},
        )
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
