from __future__ import annotations

from app.auth import OWNER_SALT, _serializer, create_session_token, read_session_token
from app.config import get_settings
from app.deps import _owner_from_cookie


def test_owner_cookie_rejected_after_password_change() -> None:
    settings = get_settings()
    token = create_session_token(settings, settings.owner_email)
    assert _owner_from_cookie(settings, token) is not None
    rotated = settings.model_copy(update={"owner_password": "rotated-owner-password"})
    assert read_session_token(rotated, token) is None
    assert _owner_from_cookie(rotated, token) is None
    fresh = create_session_token(rotated, rotated.owner_email)
    assert _owner_from_cookie(rotated, fresh) is not None


def test_owner_cookie_without_fingerprint_is_rejected() -> None:
    settings = get_settings()
    token = _serializer(settings, salt=OWNER_SALT).dumps(
        {"role": "owner", "email": settings.owner_email}
    )
    assert read_session_token(settings, token) is None
    assert _owner_from_cookie(settings, token) is None
