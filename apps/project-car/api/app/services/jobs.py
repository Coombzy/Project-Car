"""Job claim and done. Each action stores one job_events row."""

from __future__ import annotations

import re
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.models import JobEvent, JobEventKind

# Same ids and titles as the sample board in web/lib/placeholders.ts.
POSTED_JOBS: dict[str, str] = {
    "job-sweep-floor": "Sweep the shop floor",
    "job-empty-oil": "Empty the used-oil drum",
    "job-restock-towels": "Restock shop towels",
    "job-torque-wrenches": "Check and oil torque wrenches",
    "job-sort-fasteners": "Sort leftover fasteners",
    "job-take-out-recycling": "Break down cardboard",
}

OTHER_SKU = re.compile(r"^(?:TC|PT|B[1-6])-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3}$")


def _error(status: int, code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status, detail={"code": code, "message": message})


def _clean_note(note: str | None) -> str | None:
    return (note or "").strip() or None


def _require_posted_job(job_key: str) -> tuple[str, str]:
    cleaned = job_key.strip().lower()
    if OTHER_SKU.fullmatch(cleaned.upper()):
        raise _error(
            422,
            "not_a_job",
            "A tool or parts SKU is not a job. Claim a posted shop job.",
        )
    title = POSTED_JOBS.get(cleaned)
    if title is None:
        raise _error(
            422,
            "unknown_job",
            "Claim a posted shop job such as job-sweep-floor.",
        )
    return cleaned, title


def open_claim(session: Session, job_key: str) -> JobEvent | None:
    closed = select(JobEvent.claim_id).where(JobEvent.claim_id.is_not(None))
    stmt = (
        select(JobEvent)
        .where(
            JobEvent.job_key == job_key,
            JobEvent.kind == JobEventKind.CLAIM,
            JobEvent.id.not_in(closed),
        )
        .order_by(JobEvent.created_at.desc())
    )
    return session.scalars(stmt).first()


def _store(session: Session, row: JobEvent) -> JobEvent:
    session.add(row)
    try:
        session.flush()
    except IntegrityError:
        session.rollback()
        raise _error(
            409,
            "already_done",
            "That claim already has a done row.",
        ) from None
    session.refresh(row)
    return row


def claim_job(
    session: Session,
    *,
    member_id: UUID,
    job_key: str,
    note: str | None,
) -> JobEvent:
    cleaned, title = _require_posted_job(job_key)
    if open_claim(session, cleaned) is not None:
        raise _error(
            409,
            "already_claimed",
            "That job already has an open claim. Mark it done before claiming it again.",
        )
    row = JobEvent(
        member_id=member_id,
        job_key=cleaned,
        title=title,
        kind=JobEventKind.CLAIM,
        note=_clean_note(note),
        claim_id=None,
    )
    return _store(session, row)


def mark_job_done(
    session: Session,
    *,
    member_id: UUID,
    job_key: str,
    note: str | None,
) -> JobEvent:
    cleaned, title = _require_posted_job(job_key)
    claimed = open_claim(session, cleaned)
    if claimed is None:
        raise _error(
            409,
            "not_claimed",
            "That job has no open claim to mark done.",
        )
    if claimed.member_id != member_id:
        raise _error(
            409,
            "not_your_claim",
            "Only the member who claimed the job can mark it done.",
        )
    row = JobEvent(
        member_id=member_id,
        job_key=cleaned,
        title=title,
        kind=JobEventKind.DONE,
        note=_clean_note(note),
        claim_id=claimed.id,
    )
    return _store(session, row)


def list_events(session: Session) -> list[JobEvent]:
    stmt = (
        select(JobEvent)
        .options(selectinload(JobEvent.member))
        .order_by(JobEvent.created_at.desc(), JobEvent.job_key)
    )
    return list(session.scalars(stmt).all())


def list_member_events(session: Session, member_id: UUID) -> list[JobEvent]:
    stmt = (
        select(JobEvent)
        .options(selectinload(JobEvent.member))
        .where(JobEvent.member_id == member_id)
        .order_by(JobEvent.created_at.desc(), JobEvent.job_key)
    )
    return list(session.scalars(stmt).all())
