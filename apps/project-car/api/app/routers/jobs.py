"""Job ledger: a claim stores a row and done stores a row."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.deps import DbSession, MemberUser, Owner
from app.schemas import JobClaimCreate, JobDoneCreate, JobEventOut
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
