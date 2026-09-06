from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from fastapi import Response
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from app.config import Settings

OWNER_SALT = "project-car-owner"
MEMBER_SALT = "project-car-member"


@dataclass(frozen=True)
class Principal:
    role: str
    email: str
    member_id: UUID | None = None


def _serializer(settings: Settings, *, salt: str) -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(settings.session_secret, salt=salt)


def create_session_token(settings: Settings, email: str) -> str:
    return _serializer(settings, salt=OWNER_SALT).dumps({"role": "owner", "email": email})


def create_member_session_token(settings: Settings, email: str, member_id: UUID) -> str:
    return _serializer(settings, salt=MEMBER_SALT).dumps(
        {"role": "member", "email": email, "member_id": str(member_id)}
    )


def _load_payload(settings: Settings, token: str, *, salt: str) -> dict[str, Any] | None:
    try:
        payload = _serializer(settings, salt=salt).loads(token, max_age=settings.session_ttl_seconds)
    except (BadSignature, SignatureExpired):
        return None
    if not isinstance(payload, dict):
        return None
    return payload


def read_session_token(settings: Settings, token: str) -> dict[str, Any] | None:
    payload = _load_payload(settings, token, salt=OWNER_SALT)
    if payload is None or payload.get("role") != "owner":
        return None
    return payload


def read_member_session_token(settings: Settings, token: str) -> dict[str, Any] | None:
    payload = _load_payload(settings, token, salt=MEMBER_SALT)
    if payload is None or payload.get("role") != "member" or not payload.get("member_id"):
        return None
    return payload


def set_session_cookie(response: Response, settings: Settings, token: str) -> None:
    response.set_cookie(
        key=settings.cookie_name,
        value=token,
        max_age=settings.session_ttl_seconds,
        httponly=True,
        samesite="lax",
        secure=settings.cookie_secure,
        path="/",
    )


def set_member_session_cookie(response: Response, settings: Settings, token: str) -> None:
    response.set_cookie(
        key=settings.member_cookie_name,
        value=token,
        max_age=settings.session_ttl_seconds,
        httponly=True,
        samesite="lax",
        secure=settings.cookie_secure,
        path="/",
    )


def clear_session_cookie(response: Response, settings: Settings) -> None:
    response.delete_cookie(key=settings.cookie_name, path="/")


def clear_member_session_cookie(response: Response, settings: Settings) -> None:
    response.delete_cookie(key=settings.member_cookie_name, path="/")


def credentials_match(settings: Settings, email: str, password: str) -> bool:
    return email == settings.owner_email and password == settings.owner_password


def bearer_matches(settings: Settings, token: str | None) -> bool:
    if not token or not settings.owner_api_secret:
        return False
    return token == settings.owner_api_secret
