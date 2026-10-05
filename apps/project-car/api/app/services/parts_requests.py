"""Member parts requests. A PT ask stores one row. Tool checkout stays unstarted."""

from __future__ import annotations

import re
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import PartsRequest, PartsRequestStatus

PARTS_SKU = re.compile(r"^PT-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3}$")
TOOL_CHECKOUT_SKU = re.compile(r"^(?:TC|B[1-6])-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3}$")


def _error(status: int, code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status, detail={"code": code, "message": message})


def _clean_sku(sku: str) -> str:
    return sku.strip().upper()


def create_parts_request(
    session: Session,
    *,
    member_id: UUID,
    sku: str,
    note: str | None,
) -> PartsRequest:
    cleaned = _clean_sku(sku)
    if TOOL_CHECKOUT_SKU.fullmatch(cleaned):
        raise _error(
            422,
            "tool_checkout_not_started",
            "A parts request stores a PT row. Tool checkout is not started.",
        )
    if not PARTS_SKU.fullmatch(cleaned):
        raise _error(
            422,
            "invalid_parts_sku",
            "A parts request uses a PT SKU such as PT-OIL-5W30-012.",
        )
    row = PartsRequest(
        member_id=member_id,
        sku=cleaned,
        note=(note or "").strip() or None,
        status=PartsRequestStatus.OPEN,
    )
    session.add(row)
    session.flush()
    session.refresh(row)
    return row


def list_member_parts_requests(session: Session, member_id: UUID) -> list[PartsRequest]:
    stmt = (
        select(PartsRequest)
        .where(PartsRequest.member_id == member_id)
        .order_by(PartsRequest.created_at.desc(), PartsRequest.sku)
    )
    return list(session.scalars(stmt).all())


def list_parts_requests(session: Session) -> list[PartsRequest]:
    stmt = (
        select(PartsRequest)
        .options(selectinload(PartsRequest.member))
        .order_by(PartsRequest.created_at.desc(), PartsRequest.sku)
    )
    return list(session.scalars(stmt).all())
