from __future__ import annotations

from fastapi import APIRouter, HTTPException, Response

from app.auth import (
    clear_session_cookie,
    create_session_token,
    credentials_match,
    set_session_cookie,
)
from app.deps import AppSettings, Owner
from app.schemas import LoginRequest, PrincipalOut

router = APIRouter(tags=["auth"])


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


@router.get("/me", response_model=PrincipalOut)
def me(owner: Owner) -> PrincipalOut:
    return PrincipalOut(role=owner.role, email=owner.email)
