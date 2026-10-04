"""Approve, deny, draft, and read routes used by a human or an AI."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.deps import DbSession, Owner
from app.models import DraftKind
from app.schemas import (
    BookingOut,
    ChatDraftCreate,
    FillDraftCreate,
    OpenRequestsOut,
    PartsRequestCreate,
    PartsRequestOut,
    RefundRequestCreate,
    RefundRequestOut,
    ShopHoistRequestOut,
    ShopJobCreate,
    ShopJobOut,
    StaffBalanceOut,
    StaffDecisionOut,
    StaffDraftOut,
    StaffShopHoistRequestCreate,
    ToolCribExceptionCreate,
    ToolCribExceptionOut,
)
from app.services.chat import ChatError
from app.services.shop_hoist_requests import (
    approve_shop_hoist_request,
    create_shop_hoist_request,
    deny_shop_hoist_request,
)
from app.services.staff import (
    accept_chat_draft,
    accept_fill_draft,
    accept_refund_request,
    actor_of,
    complete_job,
    create_draft,
    create_job,
    create_parts_request,
    create_refund_request,
    create_tool_crib_exception,
    decide_parts_request,
    decide_tool_crib_exception,
    read_balance,
    read_open_requests,
    read_schedule,
    send_back_job,
)

router = APIRouter(tags=["staff"])


def _chat_error(exc: ChatError) -> HTTPException:
    return HTTPException(status_code=exc.status, detail={"code": exc.code, "message": exc.message})


def _member_required(message: str) -> HTTPException:
    return HTTPException(status_code=400, detail={"code": "member_required", "message": message})


def _decision(row, action, *, balance=None) -> StaffDecisionOut:
    status = row.status.value if hasattr(row.status, "value") else str(row.status)
    return StaffDecisionOut(
        request_id=row.id,
        status=status,
        actor_kind=action.actor_kind,
        actor_id=action.actor_id,
        action_id=action.id,
        action=action.action,
        booking_id=getattr(row, "booking_id", None),
        token_balance=balance,
    )


@router.post("/shop-hoist-requests", response_model=ShopHoistRequestOut, status_code=201)
def staff_create_shop_hoist_request(
    body: StaffShopHoistRequestCreate, session: DbSession, principal: Owner
) -> ShopHoistRequestOut:
    kind, actor_id = actor_of(principal)
    row = create_shop_hoist_request(
        session,
        member_id=body.member_id,
        hoist_id=body.hoist_id,
        start_at=body.start_at,
        end_at=body.end_at,
        notes=body.notes,
        created_by_kind=kind,
        created_by_id=actor_id,
    )
    return ShopHoistRequestOut.from_row(row)


@router.post("/shop-hoist-requests/{request_id}/approve", response_model=StaffDecisionOut)
def staff_approve_shop_hoist(
    request_id: UUID, session: DbSession, principal: Owner
) -> StaffDecisionOut:
    row, action = approve_shop_hoist_request(session, request_id, principal)
    return _decision(row, action, balance=row.member.token_balance)


@router.post("/shop-hoist-requests/{request_id}/deny", response_model=StaffDecisionOut)
def staff_deny_shop_hoist(
    request_id: UUID, session: DbSession, principal: Owner
) -> StaffDecisionOut:
    row, action = deny_shop_hoist_request(session, request_id, principal)
    return _decision(row, action, balance=row.member.token_balance)


@router.post("/parts-requests", response_model=PartsRequestOut, status_code=201)
def staff_create_parts_request(
    body: PartsRequestCreate, session: DbSession, principal: Owner
) -> PartsRequestOut:
    if body.member_id is None:
        raise _member_required("A parts request needs a member.")
    kind, actor_id = actor_of(principal)
    row = create_parts_request(
        session,
        member_id=body.member_id,
        sku=body.sku,
        note=body.note,
        created_by_kind=kind,
        created_by_id=actor_id,
    )
    return PartsRequestOut.model_validate(row)


@router.post("/parts-requests/{request_id}/approve", response_model=StaffDecisionOut)
def staff_approve_parts(request_id: UUID, session: DbSession, principal: Owner) -> StaffDecisionOut:
    row, action = decide_parts_request(session, request_id, principal, approve=True)
    return _decision(row, action)


@router.post("/parts-requests/{request_id}/deny", response_model=StaffDecisionOut)
def staff_deny_parts(request_id: UUID, session: DbSession, principal: Owner) -> StaffDecisionOut:
    row, action = decide_parts_request(session, request_id, principal, approve=False)
    return _decision(row, action)


@router.post("/tool-crib-exceptions", response_model=ToolCribExceptionOut, status_code=201)
def staff_create_tool_crib_exception(
    body: ToolCribExceptionCreate, session: DbSession, principal: Owner
) -> ToolCribExceptionOut:
    if body.member_id is None:
        raise _member_required("A tool crib exception needs a member.")
    kind, actor_id = actor_of(principal)
    row = create_tool_crib_exception(
        session,
        member_id=body.member_id,
        tool_code=body.tool_code,
        reason=body.reason,
        created_by_kind=kind,
        created_by_id=actor_id,
    )
    return ToolCribExceptionOut.model_validate(row)


@router.post("/tool-crib-exceptions/{request_id}/approve", response_model=StaffDecisionOut)
def staff_approve_tool_crib(
    request_id: UUID, session: DbSession, principal: Owner
) -> StaffDecisionOut:
    row, action = decide_tool_crib_exception(session, request_id, principal, approve=True)
    return _decision(row, action)


@router.post("/tool-crib-exceptions/{request_id}/deny", response_model=StaffDecisionOut)
def staff_deny_tool_crib(
    request_id: UUID, session: DbSession, principal: Owner
) -> StaffDecisionOut:
    row, action = decide_tool_crib_exception(session, request_id, principal, approve=False)
    return _decision(row, action)


@router.post("/jobs", response_model=ShopJobOut, status_code=201)
def staff_create_job(body: ShopJobCreate, session: DbSession, _principal: Owner) -> ShopJobOut:
    return ShopJobOut.model_validate(
        create_job(session, title=body.title, notes=body.notes, token_bounty=body.token_bounty)
    )


@router.post("/jobs/{job_id}/done", response_model=StaffDecisionOut)
def staff_job_done(job_id: UUID, session: DbSession, principal: Owner) -> StaffDecisionOut:
    row, action = complete_job(session, job_id, principal)
    return _decision(row, action)


@router.post("/jobs/{job_id}/send-back", response_model=StaffDecisionOut)
def staff_job_send_back(job_id: UUID, session: DbSession, principal: Owner) -> StaffDecisionOut:
    row, action = send_back_job(session, job_id, principal)
    return _decision(row, action)


@router.post("/fill/drafts", response_model=StaffDraftOut, status_code=201)
def staff_fill_draft(body: FillDraftCreate, session: DbSession, principal: Owner) -> StaffDraftOut:
    row = create_draft(session, kind=DraftKind.FILL, body=body.body, room_id=None, principal=principal)
    return StaffDraftOut.model_validate(row)


@router.post("/fill/drafts/{draft_id}/accept", response_model=StaffDecisionOut)
def staff_accept_fill(draft_id: UUID, session: DbSession, principal: Owner) -> StaffDecisionOut:
    draft, action, _count = accept_fill_draft(session, draft_id, principal)
    return _decision(draft, action)


@router.post("/chat/drafts", response_model=StaffDraftOut, status_code=201)
def staff_chat_draft(body: ChatDraftCreate, session: DbSession, principal: Owner) -> StaffDraftOut:
    try:
        row = create_draft(
            session,
            kind=DraftKind.CHAT,
            body=body.body,
            room_id=body.room_id,
            principal=principal,
        )
    except ChatError as exc:
        raise _chat_error(exc) from exc
    return StaffDraftOut.model_validate(row)


@router.post("/chat/drafts/{draft_id}/accept", response_model=StaffDecisionOut)
def staff_accept_chat(draft_id: UUID, session: DbSession, principal: Owner) -> StaffDecisionOut:
    try:
        draft, action, _message = accept_chat_draft(session, draft_id, principal)
    except ChatError as exc:
        raise _chat_error(exc) from exc
    return _decision(draft, action)


@router.post("/refund-requests", response_model=RefundRequestOut, status_code=201)
def staff_create_refund(
    body: RefundRequestCreate, session: DbSession, principal: Owner
) -> RefundRequestOut:
    return RefundRequestOut.model_validate(create_refund_request(session, body.booking_id, principal))


@router.post("/refund-requests/{request_id}/accept", response_model=StaffDecisionOut)
def staff_accept_refund(request_id: UUID, session: DbSession, principal: Owner) -> StaffDecisionOut:
    row, action = accept_refund_request(session, request_id, principal)
    return _decision(row, action)


@router.get("/staff/schedule", response_model=list[BookingOut])
def staff_schedule(session: DbSession, principal: Owner) -> list[BookingOut]:
    return [BookingOut.from_booking(row) for row in read_schedule(session, principal)]


@router.get("/staff/members/{member_id}/balance", response_model=StaffBalanceOut)
def staff_balance(member_id: UUID, session: DbSession, principal: Owner) -> StaffBalanceOut:
    member, action = read_balance(session, principal, member_id)
    return StaffBalanceOut(
        member_id=member.id,
        token_balance=member.token_balance,
        actor_kind=action.actor_kind,
        action_id=action.id,
    )


@router.get("/staff/requests", response_model=OpenRequestsOut)
def staff_open_requests(session: DbSession, principal: Owner) -> OpenRequestsOut:
    hoist, parts, tools, action = read_open_requests(session, principal)
    return OpenRequestsOut(
        shop_hoist=[ShopHoistRequestOut.from_row(row) for row in hoist],
        parts=[PartsRequestOut.model_validate(row) for row in parts],
        tool_crib=[ToolCribExceptionOut.model_validate(row) for row in tools],
        actor_kind=action.actor_kind,
        action_id=action.id,
    )
