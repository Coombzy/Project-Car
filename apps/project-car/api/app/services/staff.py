"""Staff actions shared by a human and an AI.

Same functions, same routes. The actor kind is stored with the request id.
This module does not charge a card, talk to Stripe, cut DNS, upload a Worker,
or send mail.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.auth import Principal
from app.config import get_settings
from app.models import (
    ActorKind,
    Booking,
    ChatMessage,
    DraftKind,
    DraftStatus,
    Member,
    MemberStatus,
    NotificationChannel,
    NotificationOutbox,
    NotificationStatus,
    PartsRequest,
    RefundRequest,
    ShopHoistRequest,
    ShopHoistRequestStatus,
    ShopJob,
    ShopJobStatus,
    StaffAction,
    StaffDraft,
    StaffSubject,
    ToolCribException,
)
from app.services.bookings import cancel_booking, get_booking
from app.services.chat import get_room, post_message


def _error(status: int, code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status, detail={"code": code, "message": message})


def _now() -> datetime:
    return datetime.now(timezone.utc)


def actor_of(principal: Principal) -> tuple[ActorKind, str]:
    if principal.role == "ai":
        return ActorKind.AI, principal.email
    return ActorKind.HUMAN, principal.email


def reject_own_request(principal: Principal, created_by_kind: ActorKind, created_by_id: str) -> None:
    kind, actor_id = actor_of(principal)
    if kind == ActorKind.AI and created_by_kind == ActorKind.AI and created_by_id == actor_id:
        raise _error(
            403,
            "cannot_approve_own_request",
            "An AI cannot approve a request it created.",
        )


def reject_ai(principal: Principal, *, code: str, message: str) -> None:
    if principal.role == "ai":
        raise _error(403, code, message)


def record_action(
    session: Session,
    *,
    principal: Principal,
    action: str,
    request_id: UUID | None,
    subject: StaffSubject,
) -> StaffAction:
    kind, actor_id = actor_of(principal)
    row = StaffAction(
        action=action,
        actor_kind=kind,
        actor_id=actor_id,
        request_id=request_id,
        subject_kind=subject,
    )
    session.add(row)
    session.flush()
    return row


def _active_member(session: Session, member_id: UUID) -> Member:
    member = session.get(Member, member_id)
    if member is None:
        raise _error(404, "not_found", "Member not found.")
    if member.status != MemberStatus.ACTIVE:
        raise _error(400, "member_not_bookable", "Only active members can open a request.")
    return member


def _stamp_decision(row, principal: Principal, *, status: ShopHoistRequestStatus) -> None:
    kind, actor_id = actor_of(principal)
    row.status = status
    row.decided_by_kind = kind
    row.decided_by_id = actor_id
    row.decided_at = _now()


def create_parts_request(
    session: Session,
    *,
    member_id: UUID,
    sku: str,
    note: str | None,
    created_by_kind: ActorKind,
    created_by_id: str,
) -> PartsRequest:
    _active_member(session, member_id)
    row = PartsRequest(
        member_id=member_id,
        sku=sku.strip(),
        note=note,
        status=ShopHoistRequestStatus.PENDING,
        created_by_kind=created_by_kind,
        created_by_id=created_by_id,
    )
    session.add(row)
    session.flush()
    return row


def get_parts_request(session: Session, request_id: UUID) -> PartsRequest:
    row = session.get(PartsRequest, request_id)
    if row is None:
        raise _error(404, "not_found", "Parts request not found.")
    return row


def decide_parts_request(
    session: Session, request_id: UUID, principal: Principal, *, approve: bool
) -> tuple[PartsRequest, StaffAction]:
    row = get_parts_request(session, request_id)
    if row.status != ShopHoistRequestStatus.PENDING:
        raise _error(400, "invalid_transition", "Only a pending parts request can be decided.")
    if approve:
        reject_own_request(principal, row.created_by_kind, row.created_by_id)
    _stamp_decision(
        row,
        principal,
        status=ShopHoistRequestStatus.APPROVED if approve else ShopHoistRequestStatus.DENIED,
    )
    session.add(row)
    action = record_action(
        session,
        principal=principal,
        action="approve" if approve else "deny",
        request_id=row.id,
        subject=StaffSubject.PARTS,
    )
    return row, action


def create_tool_crib_exception(
    session: Session,
    *,
    member_id: UUID,
    tool_code: str,
    reason: str | None,
    created_by_kind: ActorKind,
    created_by_id: str,
) -> ToolCribException:
    _active_member(session, member_id)
    row = ToolCribException(
        member_id=member_id,
        tool_code=tool_code.strip(),
        reason=reason,
        status=ShopHoistRequestStatus.PENDING,
        created_by_kind=created_by_kind,
        created_by_id=created_by_id,
    )
    session.add(row)
    session.flush()
    return row


def get_tool_crib_exception(session: Session, request_id: UUID) -> ToolCribException:
    row = session.get(ToolCribException, request_id)
    if row is None:
        raise _error(404, "not_found", "Tool crib exception not found.")
    return row


def decide_tool_crib_exception(
    session: Session, request_id: UUID, principal: Principal, *, approve: bool
) -> tuple[ToolCribException, StaffAction]:
    row = get_tool_crib_exception(session, request_id)
    if row.status != ShopHoistRequestStatus.PENDING:
        raise _error(400, "invalid_transition", "Only a pending tool crib exception can be decided.")
    if approve:
        reject_own_request(principal, row.created_by_kind, row.created_by_id)
    _stamp_decision(
        row,
        principal,
        status=ShopHoistRequestStatus.APPROVED if approve else ShopHoistRequestStatus.DENIED,
    )
    session.add(row)
    action = record_action(
        session,
        principal=principal,
        action="approve" if approve else "deny",
        request_id=row.id,
        subject=StaffSubject.TOOL_CRIB,
    )
    return row, action


def create_job(session: Session, *, title: str, notes: str | None, token_bounty) -> ShopJob:
    row = ShopJob(title=title.strip(), notes=notes, token_bounty=token_bounty, status=ShopJobStatus.OPEN)
    session.add(row)
    session.flush()
    return row


def get_job(session: Session, job_id: UUID) -> ShopJob:
    row = session.get(ShopJob, job_id)
    if row is None:
        raise _error(404, "not_found", "Job not found.")
    return row


def claim_job(session: Session, job_id: UUID, member_id: UUID) -> ShopJob:
    _active_member(session, member_id)
    job = get_job(session, job_id)
    if job.status not in (ShopJobStatus.OPEN, ShopJobStatus.SENT_BACK):
        raise _error(400, "job_not_open", "Only an open job can be claimed.")
    job.status = ShopJobStatus.CLAIMED
    job.claimed_by_member_id = member_id
    session.add(job)
    session.flush()
    return job


def _require_claimed(job: ShopJob) -> None:
    if job.status != ShopJobStatus.CLAIMED:
        raise _error(400, "job_not_claimed", "Only a claimed job can be finished or sent back.")


def complete_job(session: Session, job_id: UUID, principal: Principal) -> tuple[ShopJob, StaffAction]:
    job = get_job(session, job_id)
    _require_claimed(job)
    job.status = ShopJobStatus.DONE
    session.add(job)
    action = record_action(
        session,
        principal=principal,
        action="job_done",
        request_id=job.id,
        subject=StaffSubject.JOB,
    )
    return job, action


def send_back_job(session: Session, job_id: UUID, principal: Principal) -> tuple[ShopJob, StaffAction]:
    job = get_job(session, job_id)
    _require_claimed(job)
    job.status = ShopJobStatus.SENT_BACK
    session.add(job)
    action = record_action(
        session,
        principal=principal,
        action="job_send_back",
        request_id=job.id,
        subject=StaffSubject.JOB,
    )
    return job, action


def create_draft(
    session: Session,
    *,
    kind: DraftKind,
    body: str,
    room_id: UUID | None,
    principal: Principal,
) -> StaffDraft:
    cleaned = body.strip()
    if not cleaned:
        raise _error(400, "empty_draft", "A draft needs text.")
    if kind == DraftKind.CHAT:
        if room_id is None:
            raise _error(400, "room_required", "A chat draft needs a room.")
        get_room(session, room_id)
    kind_actor, actor_id = actor_of(principal)
    row = StaffDraft(
        kind=kind,
        status=DraftStatus.DRAFT,
        body=cleaned,
        room_id=room_id,
        created_by_kind=kind_actor,
        created_by_id=actor_id,
    )
    session.add(row)
    session.flush()
    record_action(
        session,
        principal=principal,
        action="draft",
        request_id=row.id,
        subject=StaffSubject.FILL_DRAFT if kind == DraftKind.FILL else StaffSubject.CHAT_DRAFT,
    )
    return row


def _get_draft(session: Session, draft_id: UUID, kind: DraftKind) -> StaffDraft:
    row = session.get(StaffDraft, draft_id)
    if row is None or row.kind != kind:
        raise _error(404, "not_found", "Draft not found.")
    return row


def accept_fill_draft(session: Session, draft_id: UUID, principal: Principal) -> tuple[StaffDraft, StaffAction, int]:
    draft = _get_draft(session, draft_id, DraftKind.FILL)
    if draft.status != DraftStatus.DRAFT:
        raise _error(400, "invalid_transition", "Only a draft can be accepted.")
    reject_own_request(principal, draft.created_by_kind, draft.created_by_id)
    members = list(
        session.scalars(select(Member).where(Member.status == MemberStatus.ACTIVE)).all()
    )
    if not members:
        raise _error(400, "no_members", "No active members to notify.")
    # Record the notice in the outbox. Do not open SMTP from this path.
    host = (get_settings().smtp_host or "").strip()
    queued = NotificationStatus.PENDING if host else NotificationStatus.SENT
    sent_at = None if host else _now()
    for member in members:
        session.add(
            NotificationOutbox(
                channel=NotificationChannel.EMAIL,
                member_id=member.id,
                to_address=member.email,
                subject="Tomorrow's open bay hours",
                body=draft.body,
                payload={"kind": "fill_draft", "draft_id": str(draft.id), "smtp": False},
                status=queued,
                dry_run=False,
                sent_at=sent_at,
            )
        )
    kind, actor_id = actor_of(principal)
    draft.status = DraftStatus.ACCEPTED
    draft.accepted_by_kind = kind
    draft.accepted_by_id = actor_id
    draft.accepted_at = _now()
    session.add(draft)
    action = record_action(
        session,
        principal=principal,
        action="accept",
        request_id=draft.id,
        subject=StaffSubject.FILL_DRAFT,
    )
    return draft, action, len(members)


def accept_chat_draft(
    session: Session, draft_id: UUID, principal: Principal
) -> tuple[StaffDraft, StaffAction, ChatMessage]:
    draft = _get_draft(session, draft_id, DraftKind.CHAT)
    if draft.status != DraftStatus.DRAFT:
        raise _error(400, "invalid_transition", "Only a draft can be accepted.")
    reject_own_request(principal, draft.created_by_kind, draft.created_by_id)
    if draft.room_id is None:
        raise _error(400, "room_required", "A chat draft needs a room.")
    room = get_room(session, draft.room_id)
    message = post_message(session, room, principal=principal, body=draft.body)
    kind, actor_id = actor_of(principal)
    draft.status = DraftStatus.ACCEPTED
    draft.accepted_by_kind = kind
    draft.accepted_by_id = actor_id
    draft.accepted_at = _now()
    session.add(draft)
    action = record_action(
        session,
        principal=principal,
        action="accept",
        request_id=draft.id,
        subject=StaffSubject.CHAT_DRAFT,
    )
    return draft, action, message


def create_refund_request(session: Session, booking_id: UUID, principal: Principal) -> RefundRequest:
    get_booking(session, booking_id)
    kind, actor_id = actor_of(principal)
    row = RefundRequest(
        booking_id=booking_id,
        status=ShopHoistRequestStatus.PENDING,
        created_by_kind=kind,
        created_by_id=actor_id,
    )
    session.add(row)
    session.flush()
    record_action(
        session,
        principal=principal,
        action="draft",
        request_id=row.id,
        subject=StaffSubject.REFUND,
    )
    return row


def accept_refund_request(session: Session, request_id: UUID, principal: Principal) -> tuple[RefundRequest, StaffAction]:
    reject_ai(
        principal,
        code="refund_requires_human",
        message="A refund is not applied until a human accepts it.",
    )
    row = session.get(RefundRequest, request_id)
    if row is None:
        raise _error(404, "not_found", "Refund request not found.")
    if row.status != ShopHoistRequestStatus.PENDING:
        raise _error(400, "invalid_transition", "Only a pending refund request can be accepted.")
    cancel_booking(session, row.booking_id)
    _stamp_decision(row, principal, status=ShopHoistRequestStatus.APPROVED)
    session.add(row)
    action = record_action(
        session,
        principal=principal,
        action="accept",
        request_id=row.id,
        subject=StaffSubject.REFUND,
    )
    return row, action


def read_schedule(session: Session, principal: Principal) -> list[Booking]:
    rows = list(
        session.scalars(
            select(Booking)
            .options(selectinload(Booking.member), selectinload(Booking.hoist))
            .order_by(Booking.start_at)
        ).all()
    )
    record_action(
        session,
        principal=principal,
        action="read",
        request_id=None,
        subject=StaffSubject.SCHEDULE,
    )
    return rows


def read_balance(session: Session, principal: Principal, member_id: UUID) -> tuple[Member, StaffAction]:
    member = session.get(Member, member_id)
    if member is None:
        raise _error(404, "not_found", "Member not found.")
    action = record_action(
        session,
        principal=principal,
        action="read",
        request_id=member.id,
        subject=StaffSubject.TOKENS,
    )
    return member, action


def read_open_requests(
    session: Session, principal: Principal
) -> tuple[list[ShopHoistRequest], list[PartsRequest], list[ToolCribException], StaffAction]:
    hoist = list(
        session.scalars(
            select(ShopHoistRequest)
            .options(selectinload(ShopHoistRequest.member), selectinload(ShopHoistRequest.hoist))
            .where(ShopHoistRequest.status == ShopHoistRequestStatus.PENDING)
            .order_by(ShopHoistRequest.start_at)
        ).all()
    )
    parts = list(
        session.scalars(
            select(PartsRequest)
            .where(PartsRequest.status == ShopHoistRequestStatus.PENDING)
            .order_by(PartsRequest.created_at)
        ).all()
    )
    tools = list(
        session.scalars(
            select(ToolCribException)
            .where(ToolCribException.status == ShopHoistRequestStatus.PENDING)
            .order_by(ToolCribException.created_at)
        ).all()
    )
    action = record_action(
        session,
        principal=principal,
        action="read",
        request_id=None,
        subject=StaffSubject.OPEN_REQUESTS,
    )
    return hoist, parts, tools, action


def outbox_count(session: Session) -> int:
    return int(session.scalar(select(func.count()).select_from(NotificationOutbox)) or 0)


def message_count(session: Session, room_id: UUID) -> int:
    return int(
        session.scalar(select(func.count()).select_from(ChatMessage).where(ChatMessage.room_id == room_id)) or 0
    )
