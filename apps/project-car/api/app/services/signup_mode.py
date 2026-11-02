"""Whether a public signup creates a member or a waitlist row."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.models import ShopSetting

SIGNUP_SELF_SERVE = "self_serve"
SIGNUP_WAITLIST = "waitlist"
SIGNUP_MODES = (SIGNUP_SELF_SERVE, SIGNUP_WAITLIST)
SIGNUP_MODE_KEY = "signup_mode"


def get_signup_mode(session: Session) -> str:
    row = session.get(ShopSetting, SIGNUP_MODE_KEY)
    if row is None or row.value not in SIGNUP_MODES:
        return SIGNUP_SELF_SERVE
    return row.value


def set_signup_mode(session: Session, mode: str) -> str:
    row = session.get(ShopSetting, SIGNUP_MODE_KEY)
    if row is None:
        row = ShopSetting(key=SIGNUP_MODE_KEY, value=mode)
        session.add(row)
    else:
        row.value = mode
        session.add(row)
    session.flush()
    return row.value
