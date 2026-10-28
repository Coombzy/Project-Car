"""Member parts requests. One open PT row per member per SKU. Tool checkout stays unstarted."""

from __future__ import annotations

import re
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import PartsOrder, PartsOrderStatus, PartsRequest, PartsRequestStatus
from app.shop_time import shop_now

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
    # Stand-in: one open request per member per cleaned SKU. Fulfilled and
    # declined rows do not block. Another member's open row does not block.
    open_id = session.scalar(
        select(PartsRequest.id)
        .where(
            PartsRequest.member_id == member_id,
            PartsRequest.sku == cleaned,
            PartsRequest.status == PartsRequestStatus.OPEN,
        )
        .limit(1)
    )
    if open_id is not None:
        raise _error(
            409,
            "already_requested",
            "This member already has an open request for that SKU.",
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


def list_parts_orders(session: Session) -> list[PartsOrder]:
    stmt = select(PartsOrder).order_by(PartsOrder.ordered_at.desc(), PartsOrder.po_number)
    return list(session.scalars(stmt).all())


# ordered -> shipped -> in_transit -> received. A later rank may be skipped.
_PARTS_ORDER_FORWARD = (
    PartsOrderStatus.ORDERED,
    PartsOrderStatus.SHIPPED,
    PartsOrderStatus.IN_TRANSIT,
    PartsOrderStatus.RECEIVED,
)


def set_parts_order_status(
    session: Session,
    order_id: UUID,
    status: PartsOrderStatus,
) -> PartsOrder:
    row = session.get(PartsOrder, order_id)
    if row is None:
        raise _error(404, "not_found", "Parts order not found.")
    current = _PARTS_ORDER_FORWARD.index(row.status)
    target = _PARTS_ORDER_FORWARD.index(status)
    if target < current:
        raise _error(
            409,
            "parts_order_backward",
            "A parts order only moves forward.",
        )
    if target == current:
        return row
    row.status = status
    now = shop_now()
    if status is PartsOrderStatus.SHIPPED and row.shipped_at is None:
        row.shipped_at = now
    if status is PartsOrderStatus.RECEIVED and row.received_at is None:
        row.received_at = now
    session.add(row)
    session.flush()
    session.refresh(row)
    return row


def set_parts_request_status(
    session: Session,
    request_id: UUID,
    status: PartsRequestStatus,
) -> PartsRequest:
    closed = {PartsRequestStatus.FULFILLED, PartsRequestStatus.DECLINED}
    if status not in closed:
        raise _error(
            422,
            "invalid_parts_request_status",
            "Owner can set a parts request to fulfilled or declined.",
        )
    row = session.scalar(
        select(PartsRequest)
        .options(selectinload(PartsRequest.member))
        .where(PartsRequest.id == request_id)
    )
    if row is None:
        raise _error(404, "not_found", "Parts request not found.")
    if row.status in closed:
        raise _error(
            409,
            "parts_request_closed",
            "A fulfilled or declined parts request stays closed.",
        )
    row.status = status
    session.add(row)
    session.flush()
    session.refresh(row)
    return row
