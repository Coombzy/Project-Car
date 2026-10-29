"""Job ledger: a claim stores a row and done stores a row."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import or_, select

from app.deps import DbSession, MemberUser, Owner
from app.models import ShopJob, ShopJobStatus
from app.schemas import JobClaimCreate, JobDoneCreate, JobEventOut, ShopJobOut
from app.services import jobs as job_service

router = APIRouter(tags=["jobs"])


def _require_member_id(principal: MemberUser):
    if principal.member_id is None:
        raise HTTPException(
            status_code=401,
            detail={"code": "unauthorized", "message": "Member authentication required."},
        )
    return principal.member_id


@router.get("/jobs/events", response_model=list[JobEventOut])
def list_job_events(session: DbSession, _principal: Owner) -> list[JobEventOut]:
    rows = job_service.list_events(session)
    return [JobEventOut.from_row(row) for row in rows]


@router.get("/member/jobs/events", response_model=list[JobEventOut])
def list_my_job_events(session: DbSession, principal: MemberUser) -> list[JobEventOut]:
    member_id = _require_member_id(principal)
    rows = job_service.list_member_events(session, member_id)
    return [JobEventOut.from_row(row) for row in rows]


@router.post("/member/jobs/claims", response_model=JobEventOut, status_code=201)
def claim_job(
    body: JobClaimCreate,
    session: DbSession,
    principal: MemberUser,
) -> JobEventOut:
    member_id = _require_member_id(principal)
    row = job_service.claim_job(
        session,
        member_id=member_id,
        job_key=body.job_key,
        note=body.note,
    )
    return JobEventOut.from_row(row)


@router.post("/member/jobs/done", response_model=JobEventOut, status_code=201)
def mark_job_done(
    body: JobDoneCreate,
    session: DbSession,
    principal: MemberUser,
) -> JobEventOut:
    member_id = _require_member_id(principal)
    row = job_service.mark_job_done(
        session,
        member_id=member_id,
        job_key=body.job_key,
        note=body.note,
    )
    return JobEventOut.from_row(row)


def _page_jobs(
    session: DbSession,
    *,
    limit: int,
    offset: int,
    member_id: UUID | None = None,
) -> list[ShopJobOut]:
    """Newest first. A member sees open jobs and jobs they claimed, nothing else."""
    stmt = select(ShopJob)
    if member_id is not None:
        stmt = stmt.where(
            or_(
                ShopJob.status == ShopJobStatus.OPEN,
                ShopJob.claimed_by_member_id == member_id,
            )
        )
    rows = session.scalars(
        stmt.order_by(ShopJob.created_at.desc(), ShopJob.id.desc()).limit(limit).offset(offset)
    ).all()
    return [ShopJobOut.model_validate(row) for row in rows]


@router.get("/jobs", response_model=list[ShopJobOut])
def list_jobs(
    session: DbSession,
    _principal: Owner,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[ShopJobOut]:
    return _page_jobs(session, limit=limit, offset=offset)


@router.get("/member/jobs", response_model=list[ShopJobOut])
def list_member_jobs(
    session: DbSession,
    principal: MemberUser,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[ShopJobOut]:
    return _page_jobs(session, limit=limit, offset=offset, member_id=_require_member_id(principal))
