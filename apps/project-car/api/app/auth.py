from __future__ import annotations

import hashlib
import hmac
import os
import secrets
import threading
import time
from base64 import urlsafe_b64decode, urlsafe_b64encode
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from fastapi import HTTPException, Response
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

# Defaults from app.config.Settings. Refused when SHOP_HOST is not loopback.
DEFAULT_OWNER_API_SECRET = "dev-owner-secret"
DEFAULT_AI_API_SECRET = "dev-ai-secret"
DEFAULT_SESSION_SECRET = "dev-session-secret-change-me"
# Keep in step with seed.LOOPBACK_HOSTS.
LOOPBACK_HOSTS = {"127.0.0.1", "localhost", "::1"}

# Eight failures inside this window lock the client IP.
_LOGIN_FAILURE_LIMIT = 8
_LOGIN_FAILURE_WINDOW_SECONDS = 15 * 60


class _LoginStamp:
    """One reserved login attempt. Success removes this same object."""

    __slots__ = ("at",)

    def __init__(self, at: float) -> None:
        self.at = at


# Reserved attempts keyed by client IP. One bucket per process.
_login_failures: dict[str, list[_LoginStamp]] = {}
_login_failures_lock = threading.Lock()


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


def secrets_equal(left: str, right: str) -> bool:
    """Constant-time compare. Unequal lengths do not match."""
    return hmac.compare_digest(left.encode("utf-8"), right.encode("utf-8"))


def member_password_matches(password_hash: str | None, password: str, shared_password: str) -> bool:
    """Own hash wins. The shared password applies only while the hash is unset."""
    if password_hash:
        return verify_password(password, password_hash)
    return secrets_equal(password, shared_password)


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
    email_ok = secrets_equal(email, settings.owner_email)
    password_ok = secrets_equal(password, settings.owner_password)
    return email_ok and password_ok


def bearer_matches(settings: Settings, token: str | None) -> bool:
    secret = settings.owner_api_secret
    if not token or not secret:
        return False
    return secrets_equal(token, secret)


def ai_bearer_matches(settings: Settings, token: str | None) -> bool:
    secret = settings.ai_api_secret
    if not token or not secret:
        return False
    return secrets_equal(token, secret)


def shop_host() -> str:
    return os.environ.get("SHOP_HOST", "127.0.0.1")


def host_is_loopback(host: str | None = None) -> bool:
    raw = shop_host() if host is None else host
    normalized = raw.strip().lower().strip("[]")
    return normalized in LOOPBACK_HOSTS


def default_secret_blocked(secret: str) -> bool:
    """True when `secret` is a dev default and SHOP_HOST is not loopback."""
    if host_is_loopback():
        return False
    is_owner = secrets_equal(secret, DEFAULT_OWNER_API_SECRET)
    is_ai = secrets_equal(secret, DEFAULT_AI_API_SECRET)
    is_session = secrets_equal(secret, DEFAULT_SESSION_SECRET)
    return is_owner or is_ai or is_session


def insecure_default_error() -> HTTPException:
    return HTTPException(
        status_code=503,
        detail={
            "code": "insecure_default",
            "message": "Dev secrets are refused when SHOP_HOST is not loopback.",
        },
    )


def reject_dev_secret(secret: str) -> None:
    if default_secret_blocked(secret):
        raise insecure_default_error()


def rate_limited_error() -> HTTPException:
    return HTTPException(
        status_code=429,
        detail={
            "code": "rate_limited",
            "message": "Too many login attempts. Try again later.",
        },
    )


def reserve_login_failure(client_ip: str) -> _LoginStamp | None:
    """Reserve one failure slot before the password check.

    The cap check and the reservation share one lock, so two overlapping
    attempts cannot both pass when this IP is one failure under the cap.
    The bucket is in-process. Each API process keeps its own counts.
    Returns the reserved stamp, or None when the IP is already at the cap.
    """
    now = time.monotonic()
    with _login_failures_lock:
        stamps = _fresh_failures(client_ip, now)
        if len(stamps) >= _LOGIN_FAILURE_LIMIT:
            return None
        stamp = _LoginStamp(now)
        stamps.append(stamp)
        _login_failures[client_ip] = stamps
        return stamp


def release_login_failure(client_ip: str, stamp: object) -> None:
    """Drop the stamp reserved for a login that succeeded."""
    with _login_failures_lock:
        current = _login_failures.get(client_ip)
        if not current:
            return
        kept = [item for item in current if item is not stamp]
        if len(kept) == len(current):
            return
        if kept:
            _login_failures[client_ip] = kept
        else:
            _login_failures.pop(client_ip, None)


def clear_login_failures() -> None:
    """Drop every IP in this process's login-failure bucket."""
    with _login_failures_lock:
        _login_failures.clear()


def _fresh_failures(client_ip: str, now: float) -> list[_LoginStamp]:
    fresh = [
        stamp
        for stamp in _login_failures.get(client_ip, ())
        if now - stamp.at <= _LOGIN_FAILURE_WINDOW_SECONDS
    ]
    if fresh:
        _login_failures[client_ip] = fresh
    else:
        _login_failures.pop(client_ip, None)
    return fresh
