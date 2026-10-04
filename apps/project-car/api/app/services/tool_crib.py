"""Crib checkout and return. Each action stores one tool_crib_events row."""

from __future__ import annotations

import re
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.models import Member, MemberStatus, ToolCribEvent, ToolCribEventKind

CRIB_SKU = re.compile(r"^TC-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3}$")
BAY_SKU = re.compile(r"^B[1-6]-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3}$")
PARTS_SKU = re.compile(r"^PT-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3}$")


def _error(status: int, code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status, detail={"code": code, "message": message})


def _clean_sku(sku: str) -> str:
    return sku.strip().upper()


def _clean_note(note: str | None) -> str | None:
    return (note or "").strip() or None


def _require_crib_sku(sku: str) -> str:
    cleaned = _clean_sku(sku)
    if BAY_SKU.fullmatch(cleaned):
        raise _error(
            422,
            "bay_kit_stays_resident",
            "Bay-kit tools stay on the cart. They do not check out through the crib.",
        )
    if PARTS_SKU.fullmatch(cleaned):
        raise _error(
            422,
            "parts_are_not_tool_checkout",
            "A PT SKU is shop stock. Crib checkout uses a TC SKU.",
        )
    if not CRIB_SKU.fullmatch(cleaned):
        raise _error(
            422,
            "invalid_crib_sku",
            "Crib checkout uses a TC SKU such as TC-FL-001.",
        )
    return cleaned


def _active_member(session: Session, member_id: UUID) -> Member:
    member = session.get(Member, member_id)
    if member is None:
        raise _error(404, "member_not_found", "That member is not in the shop.")
    if member.status != MemberStatus.ACTIVE:
        raise _error(
            403,
            "member_not_active",
            "Only an active member can check out a crib tool.",
        )
    return member


def open_checkout(session: Session, sku: str) -> ToolCribEvent | None:
    returned = select(ToolCribEvent.checkout_id).where(ToolCribEvent.checkout_id.is_not(None))
    stmt = (
        select(ToolCribEvent)
        .where(
            ToolCribEvent.sku == sku,
            ToolCribEvent.kind == ToolCribEventKind.CHECKOUT,
            ToolCribEvent.id.not_in(returned),
        )
        .order_by(ToolCribEvent.created_at.desc())
    )
    return session.scalars(stmt).first()


def _store(session: Session, row: ToolCribEvent) -> ToolCribEvent:
    session.add(row)
    try:
        session.flush()
    except IntegrityError:
        session.rollback()
        raise _error(
            409,
            "already_returned",
            "That checkout already has a return row.",
        ) from None
    session.refresh(row)
    return row


def checkout_tool(
    session: Session,
    *,
    member_id: UUID,
    sku: str,
    note: str | None,
) -> ToolCribEvent:
    cleaned = _require_crib_sku(sku)
    member = _active_member(session, member_id)
    if open_checkout(session, cleaned) is not None:
        raise _error(
            409,
            "already_checked_out",
            "That crib tool already has an open checkout. Return it before checking it out again.",
        )
    row = ToolCribEvent(
        member_id=member.id,
        sku=cleaned,
        kind=ToolCribEventKind.CHECKOUT,
        note=_clean_note(note),
        checkout_id=None,
    )
    return _store(session, row)


def return_tool(session: Session, *, sku: str, note: str | None) -> ToolCribEvent:
    cleaned = _require_crib_sku(sku)
    checked_out = open_checkout(session, cleaned)
    if checked_out is None:
        raise _error(
            409,
            "not_checked_out",
            "That crib tool has no open checkout to return.",
        )
    row = ToolCribEvent(
        member_id=checked_out.member_id,
        sku=checked_out.sku,
        kind=ToolCribEventKind.RETURN,
        note=_clean_note(note),
        checkout_id=checked_out.id,
    )
    return _store(session, row)


def list_events(session: Session) -> list[ToolCribEvent]:
    stmt = (
        select(ToolCribEvent)
        .options(selectinload(ToolCribEvent.member))
        .order_by(ToolCribEvent.created_at.desc(), ToolCribEvent.sku)
    )
    return list(session.scalars(stmt).all())
