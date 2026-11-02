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
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.models import OwnerSessionEpoch

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

# Defaults a dev env used to ship. Refused unless SHOP_DEV_MODE is on.
# Binding loopback does not make them safe: production sits on 127.0.0.1.
DEFAULT_OWNER_API_SECRET = "dev-owner-secret"
DEFAULT_AI_API_SECRET = "dev-ai-secret"
DEFAULT_SESSION_SECRET = "dev-session-secret-change-me"
DEFAULT_PROXY_SECRET = "dev-proxy-secret"
_SECRET_MIN_LENGTH = 32
_PASSWORD_MIN_LENGTH = 12
# Shared member password from app.config.Settings. An unhashed member cannot
# use this value when SHOP_HOST is not loopback. That refusal is a failed
# login (401), not the 503 insecure_default path used for the secrets above.
DEFAULT_MEMBER_DEMO_PASSWORD = "changeme"
# Keep in step with seed.LOOPBACK_HOSTS.
LOOPBACK_HOSTS = {"127.0.0.1", "localhost", "::1"}

# Eight failures inside this window lock one realm on one client IP.
_LOGIN_FAILURE_LIMIT = 8
_LOGIN_FAILURE_WINDOW_SECONDS = 15 * 60
# After this many failures of one account, from any IPs, wait 1, 2, 4… minutes.
_ACCOUNT_FAILURE_LIMIT = 5
_ACCOUNT_BACKOFF_CAP_SECONDS = 15 * 60
# 60 * 2**4 is 960 seconds, already past the cap. A larger shift overflows float.
_ACCOUNT_BACKOFF_MAX_SHIFT = 4


class _LoginStamp:
    """One reserved login attempt. Success removes this same object."""

    __slots__ = ("at", "realm", "account")

    def __init__(self, at: float, realm: str, account: str) -> None:
        self.at = at
        self.realm = realm
        self.account = account


# IP buckets are (realm, client IP). Account buckets are (realm, email).
_ip_failures: dict[tuple[str, str], list[_LoginStamp]] = {}
_account_failures: dict[tuple[str, str], list[_LoginStamp]] = {}
_login_failures_lock = threading.Lock()


@dataclass(frozen=True)
class Principal:
    role: str
    email: str
    member_id: UUID | None = None


def _serializer(settings: Settings, *, salt: str) -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(settings.session_secret, salt=salt)


def create_session_token(settings: Settings, email: str, *, epoch: int) -> str:
    return _serializer(settings, salt=OWNER_SALT).dumps(
        {
            "role": "owner",
            "email": email,
            "pwd_fp": owner_password_fingerprint(settings, settings.owner_password),
            "epoch": epoch,
        }
    )


def owner_password_fingerprint(settings: Settings, password: str) -> str:
    """Short keyed digest of the owner password. Not the password."""
    digest = hmac.new(
        settings.session_secret.encode("utf-8"),
        b"owner-password-fp\0" + password.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return digest[:_PASSWORD_FINGERPRINT_HEX]


def current_owner_epoch(session: Session) -> int:
    """Epoch 1 until a row exists. Logout stores the next value."""
    row = session.get(OwnerSessionEpoch, 1)
    if row is None:
        return 1
    return int(row.epoch)


def bump_owner_epoch(session: Session) -> int:
    """Invalidate every owner cookie. The bearer secret is not a session."""
    row = session.get(OwnerSessionEpoch, 1)
    if row is None:
        row = OwnerSessionEpoch(id=1, epoch=2)
        session.add(row)
    else:
        row.epoch = int(row.epoch) + 1
    session.flush()
    return int(row.epoch)


def owner_session_current(settings: Settings, session: Session, payload: dict[str, Any]) -> bool:
    """False after logout (epoch) or after the owner password changes (pwd_fp)."""
    expected = owner_password_fingerprint(settings, settings.owner_password)
    presented = payload.get("pwd_fp")
    if not isinstance(presented, str) or len(presented) != len(expected):
        return False
    if not hmac.compare_digest(presented, expected):
        return False
    token_epoch = payload.get("epoch")
    if isinstance(token_epoch, bool) or not isinstance(token_epoch, int):
        return False
    return token_epoch == current_owner_epoch(session)


# Truncated HMAC hex. Long enough to change when the hash changes, short
# enough that the cookie does not carry the hash.
_PASSWORD_FINGERPRINT_HEX = 16


def password_fingerprint(settings: Settings, password_hash: str | None) -> str:
    """Short keyed digest of the stored hash, or ``none`` when unset.

    The digest is not the hash and not the password. Login stores it in the
    member session so a later password change no longer matches.
    """
    if not password_hash:
        return "none"
    digest = hmac.new(
        settings.session_secret.encode("utf-8"),
        b"member-password-fp\0" + password_hash.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return digest[:_PASSWORD_FINGERPRINT_HEX]


def member_password_fingerprint_matches(
    settings: Settings, presented: object, password_hash: str | None
) -> bool:
    """True when the session value is the member's current hash fingerprint."""
    expected = password_fingerprint(settings, password_hash)
    if not isinstance(presented, str) or len(presented) != len(expected):
        return False
    return hmac.compare_digest(presented, expected)


def create_member_session_token(
    settings: Settings,
    email: str,
    member_id: UUID,
    password_hash: str | None,
) -> str:
    return _serializer(settings, salt=MEMBER_SALT).dumps(
        {
            "role": "member",
            "email": email,
            "member_id": str(member_id),
            "pwd_fp": password_fingerprint(settings, password_hash),
        }
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


def resolved_cookie_secure(settings: Settings) -> bool:
    """Secure by default. An explicit bool, or dev mode, opts out."""
    if settings.cookie_secure is not None:
        return bool(settings.cookie_secure)
    if shop_dev_mode():
        return False
    return True


def set_session_cookie(response: Response, settings: Settings, token: str) -> None:
    response.set_cookie(
        key=settings.cookie_name,
        value=token,
        max_age=settings.session_ttl_seconds,
        httponly=True,
        samesite="lax",
        secure=resolved_cookie_secure(settings),
        path="/",
    )


def set_member_session_cookie(response: Response, settings: Settings, token: str) -> None:
    response.set_cookie(
        key=settings.member_cookie_name,
        value=token,
        max_age=settings.session_ttl_seconds,
        httponly=True,
        samesite="lax",
        secure=resolved_cookie_secure(settings),
        path="/",
    )


def clear_session_cookie(response: Response, settings: Settings) -> None:
    response.delete_cookie(
        key=settings.cookie_name,
        path="/",
        secure=resolved_cookie_secure(settings),
    )


def clear_member_session_cookie(response: Response, settings: Settings) -> None:
    response.delete_cookie(
        key=settings.member_cookie_name,
        path="/",
        secure=resolved_cookie_secure(settings),
    )


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
    """Own hash wins. The shared password applies only while the hash is unset.

    Off loopback, the default shared password does not match an unhashed member.
    A non-default shared password still does. A stored hash is unchanged.
    """
    if password_hash:
        return verify_password(password, password_hash)
    if not host_is_loopback() and secrets_equal(shared_password, DEFAULT_MEMBER_DEMO_PASSWORD):
        return False
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
    # The demo owner password is never a login, including on loopback, unless
    # this process was started with SHOP_DEV_MODE.
    if not shop_dev_mode() and secrets_equal(password, DEFAULT_MEMBER_DEMO_PASSWORD):
        return False
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


def shop_dev_mode() -> bool:
    """True only when SHOP_DEV_MODE is explicitly on. The bind address is ignored.

    Settings loads the flag from the process environment and from `.env`.
    uvicorn does not export that file, so a copied `.env.example` still counts.
    """
    return bool(get_settings().shop_dev_mode)


def default_secret_blocked(secret: str) -> bool:
    """True when `secret` is a dev default and SHOP_DEV_MODE is not set."""
    if shop_dev_mode():
        return False
    if not secret:
        return True
    is_owner = secrets_equal(secret, DEFAULT_OWNER_API_SECRET)
    is_ai = secrets_equal(secret, DEFAULT_AI_API_SECRET)
    is_session = secrets_equal(secret, DEFAULT_SESSION_SECRET)
    return is_owner or is_ai or is_session


def insecure_default_error() -> HTTPException:
    return HTTPException(
        status_code=503,
        detail={
            "code": "insecure_default",
            "message": "Dev secrets are refused unless SHOP_DEV_MODE is set.",
        },
    )


def assert_runtime_secrets(settings: Settings) -> None:
    """Refuse a forwarded-for client IP header, and weak secrets outside dev mode.

    The error names the setting. It does not include the value.
    """
    header = settings.client_ip_header.strip()
    if header.lower() == "x-forwarded-for":
        raise RuntimeError("CLIENT_IP_HEADER must not be X-Forwarded-For")
    if shop_dev_mode():
        return
    _require_secret(
        "owner_api_secret",
        settings.owner_api_secret,
        _SECRET_MIN_LENGTH,
        (DEFAULT_OWNER_API_SECRET,),
    )
    _require_secret(
        "ai_api_secret",
        settings.ai_api_secret,
        _SECRET_MIN_LENGTH,
        (DEFAULT_AI_API_SECRET,),
    )
    _require_secret(
        "session_secret",
        settings.session_secret,
        _SECRET_MIN_LENGTH,
        (DEFAULT_SESSION_SECRET,),
    )
    _require_secret(
        "owner_password",
        settings.owner_password,
        _PASSWORD_MIN_LENGTH,
        (DEFAULT_MEMBER_DEMO_PASSWORD,),
    )
    if settings.shop_proxy_secret:
        _require_secret(
            "shop_proxy_secret",
            settings.shop_proxy_secret,
            _SECRET_MIN_LENGTH,
            (DEFAULT_PROXY_SECRET,),
        )


def _require_secret(name: str, value: str, minimum: int, defaults: tuple[str, ...]) -> None:
    refused = len(value) < minimum or value.startswith("CHANGE_ME")
    if not refused:
        for default in defaults:
            if secrets_equal(value, default):
                refused = True
                break
    if refused:
        raise RuntimeError(f"insecure default secret: {name}")


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


def reserve_login_failure(
    client_ip: str, realm: str = "owner", account: str | None = None
) -> _LoginStamp | None:
    """Reserve one failure slot before the password check.

    The cap check and the reservation share one lock, so two overlapping
    attempts cannot both pass when this IP is one failure under the cap.
    Realm is owner or member, so one realm cannot fill the other's IP bucket.
    A non-empty account also counts across IPs and backs off after five
    failures. The buckets are in-process. Each API process keeps its own counts.
    Returns the reserved stamp, or None when the attempt is limited.
    """
    normalized = (account or "").strip().lower()
    now = time.monotonic()
    with _login_failures_lock:
        if normalized and _account_is_blocked(realm, normalized, now):
            return None
        stamps = _fresh_ip(realm, client_ip, now)
        if len(stamps) >= _LOGIN_FAILURE_LIMIT:
            return None
        stamp = _LoginStamp(now, realm, normalized)
        stamps.append(stamp)
        _ip_failures[(realm, client_ip)] = stamps
        if normalized:
            account_stamps = _fresh_account(realm, normalized, now)
            account_stamps.append(stamp)
            _account_failures[(realm, normalized)] = account_stamps
        return stamp


def release_login_failure(client_ip: str, stamp: object) -> None:
    """Drop the stamp reserved for a login that succeeded."""
    if not isinstance(stamp, _LoginStamp):
        return
    with _login_failures_lock:
        key = (stamp.realm, client_ip)
        current = _ip_failures.get(key)
        if current:
            kept = [item for item in current if item is not stamp]
            if len(kept) == len(current):
                pass
            elif kept:
                _ip_failures[key] = kept
            else:
                _ip_failures.pop(key, None)
        if stamp.account:
            _account_failures.pop((stamp.realm, stamp.account), None)


def clear_login_failures() -> None:
    """Drop every login-failure bucket in this process."""
    with _login_failures_lock:
        _ip_failures.clear()
        _account_failures.clear()


def _fresh_ip(realm: str, client_ip: str, now: float) -> list[_LoginStamp]:
    return _fresh_bucket(_ip_failures, (realm, client_ip), now)


def _fresh_account(realm: str, account: str, now: float) -> list[_LoginStamp]:
    return _fresh_bucket(_account_failures, (realm, account), now)


def _fresh_bucket(
    store: dict[tuple[str, str], list[_LoginStamp]],
    key: tuple[str, str],
    now: float,
) -> list[_LoginStamp]:
    fresh = [
        stamp
        for stamp in store.get(key, ())
        if now - stamp.at <= _LOGIN_FAILURE_WINDOW_SECONDS
    ]
    if fresh:
        store[key] = fresh
    else:
        store.pop(key, None)
    return fresh


def _account_backoff_seconds(failure_count: int) -> float:
    """1, 2, 4… minutes after five failures, capped at 15 minutes."""
    if failure_count < _ACCOUNT_FAILURE_LIMIT:
        return 0.0
    shift = min(failure_count - _ACCOUNT_FAILURE_LIMIT, _ACCOUNT_BACKOFF_MAX_SHIFT)
    seconds = 60 * (2 ** shift)
    return min(float(seconds), float(_ACCOUNT_BACKOFF_CAP_SECONDS))


def _account_is_blocked(realm: str, account: str, now: float) -> bool:
    stamps = _fresh_account(realm, account, now)
    if len(stamps) < _ACCOUNT_FAILURE_LIMIT:
        return False
    wait = _account_backoff_seconds(len(stamps))
    latest = max(stamp.at for stamp in stamps)
    return now - latest < wait
