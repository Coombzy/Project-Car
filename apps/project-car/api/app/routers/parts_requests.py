"""Parts requests: a member PT ask stores a row. Not tool checkout."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.deps import DbSession, MemberUser, Owner
from app.schemas import PartsRequestCreate, PartsRequestOut
from app.services import parts_requests as parts_request_service

router = APIRouter(tags=["parts-requests"])


def _require_member_id(principal: MemberUser):
    if principal.member_id is None:
        raise HTTPException(
            status_code=401,
            detail={"code": "unauthorized", "message": "Member authentication required."},
        )
    return principal.member_id


@router.get("/member/parts-requests", response_model=list[PartsRequestOut])
def list_my_parts_requests(session: DbSession, principal: MemberUser) -> list[PartsRequestOut]:
    member_id = _require_member_id(principal)
    rows = parts_request_service.list_member_parts_requests(session, member_id)
    return [PartsRequestOut.from_row(row) for row in rows]


@router.post("/member/parts-requests", response_model=PartsRequestOut, status_code=201)
def create_my_parts_request(
    body: PartsRequestCreate,
    session: DbSession,
    principal: MemberUser,
) -> PartsRequestOut:
    member_id = _require_member_id(principal)
    row = parts_request_service.create_parts_request(
        session,
        member_id=member_id,
        sku=body.sku,
        note=body.note,
    )
    return PartsRequestOut.from_row(row)


@router.get("/parts-requests", response_model=list[PartsRequestOut])
def list_parts_requests(session: DbSession, _principal: Owner) -> list[PartsRequestOut]:
    rows = parts_request_service.list_parts_requests(session)
    return [PartsRequestOut.from_row(row) for row in rows]
