"""Public signup. Self-serve creates the member. Waitlist is the fallback."""

from __future__ import annotations

import threading
import time
from decimal import Decimal
from typing import Literal
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel, EmailStr, Field, field_validator
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.auth import create_member_session_token, hash_password, set_member_session_cookie
from app.client_ip import client_ip
from app.config import get_settings
from app.deps import AppSettings, DbSession, Owner
from app.models import Member, MemberStatus, MembershipTier, TokenTransactionKind
from app.routers.members import MEMBER_PASSWORD_MIN_LENGTH
from app.routers.waitlist import create_waitlist_entry
from app.schemas import WaitlistCreate
from app.services.signup_mode import SIGNUP_SELF_SERVE, SIGNUP_WAITLIST, get_signup_mode, set_signup_mode
from app.services.staff import reject_ai
from app.services.tokens import apply_ledger

router = APIRouter(tags=["signup"])

_SIGNUP_CREATE_LIMIT = 8
_SIGNUP_CREATE_WINDOW_SECONDS = 15 * 60


class _CreateStamp:
    __slots__ = ("at",)

    def __init__(self, at: float) -> None:
        self.at = at


_signup_creates: dict[str, list[_CreateStamp]] = {}
_signup_creates_lock = threading.Lock()


class SignupModeOut(BaseModel):
    mode: Literal["self_serve", "waitlist"]


class SignupModeUpdate(BaseModel):
    mode: Literal["self_serve", "waitlist"]


class SignupCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=40)
    password: str | None = None
    tier_name: str = "basic"
    notes: str | None = Field(default=None, max_length=2000)

    @field_validator("name")
    @classmethod
    def strip_name(cls, value: str) -> str:
        return value.strip()

    @field_validator("tier_name")
    @classmethod
    def normalize_tier(cls, value: str) -> str:
        cleaned = value.strip().lower()
        if not cleaned:
            raise ValueError("Tier is required.")
        return cleaned

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip().lower()
        return value


class SignupOut(BaseModel):
    mode: Literal["self_serve", "waitlist"]
    member_id: UUID | None = None
    email: str
    tier_name: str | None = None
    waitlist_id: UUID | None = None


def _http(status: int, code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status, detail={"code": code, "message": message})


def _reserve_signup(client: str) -> _CreateStamp | None:
    now = time.monotonic()
    with _signup_creates_lock:
        fresh = [
            stamp
            for stamp in _signup_creates.get(client, ())
            if now - stamp.at <= _SIGNUP_CREATE_WINDOW_SECONDS
        ]
        if len(fresh) >= _SIGNUP_CREATE_LIMIT:
            _signup_creates[client] = fresh
            return None
        stamp = _CreateStamp(now)
        fresh.append(stamp)
        _signup_creates[client] = fresh
        return stamp


def _release_signup(client: str, stamp: _CreateStamp) -> None:
    with _signup_creates_lock:
        current = _signup_creates.get(client)
        if not current:
            return
        kept = [item for item in current if item is not stamp]
        if kept:
            _signup_creates[client] = kept
        else:
            _signup_creates.pop(client, None)


@router.get("/signup-mode", response_model=SignupModeOut)
def read_signup_mode(session: DbSession) -> SignupModeOut:
    mode = get_signup_mode(session)
    if mode == SIGNUP_WAITLIST:
        return SignupModeOut(mode=SIGNUP_WAITLIST)
    return SignupModeOut(mode=SIGNUP_SELF_SERVE)


@router.patch("/signup-mode", response_model=SignupModeOut)
def update_signup_mode(body: SignupModeUpdate, session: DbSession, owner: Owner) -> SignupModeOut:
    reject_ai(
        owner,
        code="signup_mode_requires_human",
        message="An AI cannot change how people sign up.",
    )
    saved = set_signup_mode(session, body.mode)
    if saved == SIGNUP_WAITLIST:
        return SignupModeOut(mode=SIGNUP_WAITLIST)
    return SignupModeOut(mode=SIGNUP_SELF_SERVE)


@router.post("/signup", response_model=SignupOut, status_code=201)
def signup(
    body: SignupCreate,
    request: Request,
    response: Response,
    session: DbSession,
    settings: AppSettings,
) -> SignupOut:
    mode = get_signup_mode(session)
    if mode == SIGNUP_WAITLIST:
        entry = create_waitlist_entry(
            WaitlistCreate(name=body.name, email=body.email, phone=body.phone, notes=body.notes),
            request,
            session,
            settings,
        )
        return SignupOut(mode=SIGNUP_WAITLIST, email=str(body.email), waitlist_id=entry.id)

    password = body.password or ""
    if len(password) < MEMBER_PASSWORD_MIN_LENGTH or password.isspace():
        raise _http(
            422,
            "password_too_short",
            f"Password must be at least {MEMBER_PASSWORD_MIN_LENGTH} characters and cannot be only spaces.",
        )

    tier = session.get(MembershipTier, body.tier_name)
    if tier is None:
        raise _http(400, "unknown_tier", "Unknown membership tier.")

    email = str(body.email)
    existing = session.scalar(select(Member).where(Member.email == email))
    if existing is not None:
        raise _http(409, "duplicate_email", "A member with that email already exists.")

    address = client_ip(request, get_settings().client_ip_header)
    stamp = _reserve_signup(address)
    if stamp is None:
        raise _http(429, "rate_limited", "Too many signups. Try again later.")

    member = Member(
        name=body.name,
        email=email,
        phone=body.phone,
        tier_name=tier.name,
        status=MemberStatus.ACTIVE,
        token_balance=Decimal("0"),
        deposit_balance=Decimal("0"),
        password_hash=hash_password(password),
    )
    session.add(member)
    try:
        session.flush()
    except IntegrityError:
        session.rollback()
        _release_signup(address, stamp)
        raise _http(409, "duplicate_email", "A member with that email already exists.") from None

    if tier.included_tokens:
        apply_ledger(
            session,
            member,
            kind=TokenTransactionKind.MONTHLY_ALLOCATION,
            amount=Decimal(tier.included_tokens),
            note=f"Initial {tier.display_name} allocation",
        )

    token = create_member_session_token(settings, member.email, member.id, member.password_hash)
    set_member_session_cookie(response, settings, token)
    return SignupOut(
        mode=SIGNUP_SELF_SERVE,
        member_id=member.id,
        email=member.email,
        tier_name=tier.name,
    )
