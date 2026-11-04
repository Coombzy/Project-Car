"""Crib ledger: a checkout stores a row and a return stores a row."""

from __future__ import annotations

from fastapi import APIRouter, Query

from app.deps import DbSession, Owner
from app.schemas import ToolCribCheckoutCreate, ToolCribEventOut, ToolCribReturnCreate
from app.services import tool_crib as tool_crib_service

router = APIRouter(prefix="/tool-crib", tags=["tool-crib"])


@router.get("/events", response_model=list[ToolCribEventOut])
def list_tool_crib_events(
    session: DbSession,
    _principal: Owner,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[ToolCribEventOut]:
    rows = tool_crib_service.list_events(session, limit=limit, offset=offset)
    return [ToolCribEventOut.from_row(row) for row in rows]


@router.post("/checkouts", response_model=ToolCribEventOut, status_code=201)
def checkout_crib_tool(
    body: ToolCribCheckoutCreate,
    session: DbSession,
    _principal: Owner,
) -> ToolCribEventOut:
    row = tool_crib_service.checkout_tool(
        session,
        member_id=body.member_id,
        sku=body.sku,
        note=body.note,
    )
    return ToolCribEventOut.from_row(row)


@router.post("/returns", response_model=ToolCribEventOut, status_code=201)
def return_crib_tool(
    body: ToolCribReturnCreate,
    session: DbSession,
    _principal: Owner,
) -> ToolCribEventOut:
    row = tool_crib_service.return_tool(session, sku=body.sku, note=body.note)
    return ToolCribEventOut.from_row(row)
