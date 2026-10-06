from __future__ import annotations

import hashlib
import hmac
import secrets
from base64 import urlsafe_b64decode, urlsafe_b64encode
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from fastapi import Response
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from app.config import Settings

# Interactive scrypt (RFC 7914). N=2**14 stays under OpenSSL's default memory cap.
_SCRYPT_N = 2**14
_SCRYPT_R = 8
_SCRYPT_P = 1
_SCRYPT_DKLEN = 32
_SCRYPT_SALT_BYTES = 16
_SCRYPT_MAXMEM = 32 * 1024 * 1024
_SCRYPT_MAX_N = 2**20
_SCRYPT_MAX_R = 16
_SCRYPT_MAX_P = 2

OWNER_SALT = "project-car-owner"
MEMBER_SALT = "project-car-member"
# Fixed scrypt so a missing member pays the same cost as a wrong password.
DUMMY_MEMBER_PASSWORD_HASH = (
    "scrypt$16384$8$1$FeNmoqWBAr3KRneA6j80ng==$uwxOA_jxxH2giYqHXgZwA_8rV14Jas_WtgL8ML9cTMo="
)


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


def hash_password(password: str) -> str:
    """Salted scrypt hash. The return value is not the plaintext password."""
    salt = secrets.token_bytes(_SCRYPT_SALT_BYTES)
    derived = hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=_SCRYPT_N,
        r=_SCRYPT_R,
        p=_SCRYPT_P,
        dklen=_SCRYPT_DKLEN,
        maxmem=_SCRYPT_MAXMEM,
    )
    salt_b64 = urlsafe_b64encode(salt).decode("ascii")
    hash_b64 = urlsafe_b64encode(derived).decode("ascii")
    return f"scrypt${_SCRYPT_N}${_SCRYPT_R}${_SCRYPT_P}${salt_b64}${hash_b64}"


def verify_password(password: str, stored: str) -> bool:
    """True when password matches a stored scrypt hash. Compare is constant-time."""
    parsed = _parse_scrypt(stored)
    if parsed is None:
        return False
    n, r, p, salt, expected = parsed
    try:
        derived = hashlib.scrypt(
            password.encode("utf-8"),
            salt=salt,
            n=n,
            r=r,
            p=p,
            dklen=len(expected),
            maxmem=_SCRYPT_MAXMEM,
        )
    except (ValueError, TypeError, MemoryError):
        return False
    return hmac.compare_digest(derived, expected)


def member_password_matches(password_hash: str | None, password: str, shared_password: str) -> bool:
    """Own hash wins. The shared password applies only while the hash is unset."""
    if password_hash:
        return verify_password(password, password_hash)
    return password == shared_password


def _parse_scrypt(stored: str) -> tuple[int, int, int, bytes, bytes] | None:
    parts = stored.split("$")
    if len(parts) != 6 or parts[0] != "scrypt":
        return None
    try:
        n = int(parts[1])
        r = int(parts[2])
        p = int(parts[3])
        salt = urlsafe_b64decode(parts[4].encode("ascii"))
        expected = urlsafe_b64decode(parts[5].encode("ascii"))
    except (ValueError, TypeError):
        return None
    if n < 2 or n > _SCRYPT_MAX_N or r < 1 or r > _SCRYPT_MAX_R or p < 1 or p > _SCRYPT_MAX_P:
        return None
    if len(salt) < 8 or len(expected) < 16:
        return None
    return n, r, p, salt, expected


def credentials_match(settings: Settings, email: str, password: str) -> bool:
    return email == settings.owner_email and password == settings.owner_password


def bearer_matches(settings: Settings, token: str | None) -> bool:
    if not token or not settings.owner_api_secret:
        return False
    return token == settings.owner_api_secret


def ai_bearer_matches(settings: Settings, token: str | None) -> bool:
    if not token or not settings.ai_api_secret:
        return False
    return token == settings.ai_api_secret
