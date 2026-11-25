from __future__ import annotations

from app.auth import OWNER_SALT, Principal, _serializer, password_fingerprint
from app.config import get_settings
from app.deps import _owner_from_cookie


def _token(payload: dict) -> str:
    settings = get_settings()
    body = {
        **payload,
        "pwd_fp": password_fingerprint(settings, settings.owner_password),
    }
    return _serializer(settings, salt=OWNER_SALT).dumps(body)


def test_owner_cookie_without_email_is_rejected() -> None:
    settings = get_settings()
    assert _owner_from_cookie(settings, _token({"role": "owner"})) is None


def test_owner_cookie_with_blank_email_is_rejected() -> None:
    settings = get_settings()
    token = _token({"role": "owner", "email": ""})
    assert _owner_from_cookie(settings, token) is None


def test_owner_cookie_with_foreign_email_is_rejected() -> None:
    settings = get_settings()
    token = _token({"role": "owner", "email": "intruder@example.com"})
    assert _owner_from_cookie(settings, token) is None


def test_owner_cookie_with_owner_email_is_accepted() -> None:
    settings = get_settings()
    token = _token({"role": "owner", "email": settings.owner_email})
    principal = _owner_from_cookie(settings, token)
    assert principal == Principal(role="owner", email=settings.owner_email)
