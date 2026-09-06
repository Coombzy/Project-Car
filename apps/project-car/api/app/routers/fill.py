"""Owner fill-the-gaps preview, publish, and member notify."""

from __future__ import annotations

from decimal import Decimal

from fastapi import APIRouter, HTTPException, Query

from app.deps import DbSession, Owner
from app.schemas import FillNotifyOut, FillNotifyRequest, FillPreviewOut, NotificationOutboxOut
from app.services.fill import FillError, snapshot_next_day, upsert_published_offer
from app.services.notify import NotifyError, enqueue_fill_campaign, list_outbox, parse_channels

router = APIRouter(tags=["fill"])


def _error(status: int, code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status, detail={"code": code, "message": message})


@router.get("/fill/preview", response_model=FillPreviewOut)
def preview_fill(
    session: DbSession,
    _owner: Owner,
    discount_pct: Decimal | None = Query(default=None),
) -> FillPreviewOut:
    snapshot = snapshot_next_day(session, discount_override=discount_pct, prefer_published=discount_pct is None)
    return FillPreviewOut.from_snapshot(snapshot)


@router.get("/fill/outbox", response_model=list[NotificationOutboxOut])
def fill_outbox(
    session: DbSession,
    _owner: Owner,
    limit: int = Query(default=50, ge=1, le=200),
) -> list[NotificationOutboxOut]:
    return [NotificationOutboxOut.model_validate(row) for row in list_outbox(session, limit=limit)]


@router.post("/fill/notify", response_model=FillNotifyOut)
def notify_fill(body: FillNotifyRequest, session: DbSession, _owner: Owner) -> FillNotifyOut:
    try:
        channels = parse_channels(body.channels)
        snapshot = snapshot_next_day(
            session,
            discount_override=body.discount_pct,
            prefer_published=body.discount_pct is None,
        )
        offer = None
        published = False
        if not body.dry_run:
            offer = upsert_published_offer(session, snapshot)
            published = True
        rows = enqueue_fill_campaign(
            session,
            snapshot,
            channels=channels,
            dry_run=body.dry_run,
            offer=offer,
        )
    except (FillError, NotifyError) as exc:
        raise _error(400, exc.code, exc.message) from exc
    return FillNotifyOut(
        preview=FillPreviewOut.from_snapshot(snapshot),
        dry_run=body.dry_run,
        published=published,
        queued=len(rows),
        notifications=[NotificationOutboxOut.model_validate(row) for row in rows],
    )
