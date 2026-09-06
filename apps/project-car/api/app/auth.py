from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from fastapi import Response
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from app.config import Settings


@dataclass(frozen=True)
class Principal:
    role: str
    email: str


def _serializer(settings: Settings) -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(settings.session_secret, salt="project-car-owner")


def create_session_token(settings: Settings, email: str) -> str:
    return _serializer(settings).dumps({"role": "owner", "email": email})


def read_session_token(settings: Settings, token: str) -> dict[str, Any] | None:
    try:
        payload = _serializer(settings).loads(token, max_age=settings.session_ttl_seconds)
    except (BadSignature, SignatureExpired):
        return None
    if not isinstance(payload, dict) or payload.get("role") != "owner":
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


def clear_session_cookie(response: Response, settings: Settings) -> None:
    response.delete_cookie(key=settings.cookie_name, path="/")


def credentials_match(settings: Settings, email: str, password: str) -> bool:
    return email == settings.owner_email and password == settings.owner_password


def bearer_matches(settings: Settings, token: str | None) -> bool:
    if not token or not settings.owner_api_secret:
        return False
    return token == settings.owner_api_secret
