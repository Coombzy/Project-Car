from __future__ import annotations

from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.deps import DbSession, Owner
from app.models import MembershipTier
from app.schemas import TierCreate, TierOut, TierPatch

router = APIRouter(tags=["tiers"])


@router.get("/tiers", response_model=list[TierOut])
def list_tiers(session: DbSession, _owner: Owner) -> list[TierOut]:
    rows = session.scalars(select(MembershipTier).order_by(MembershipTier.name)).all()
    return [TierOut.model_validate(row) for row in rows]


@router.post("/tiers", response_model=TierOut, status_code=201)
def create_tier(body: TierCreate, session: DbSession, _owner: Owner) -> TierOut:
    row = MembershipTier(
        name=body.name,
        display_name=body.display_name,
        price=body.price,
        included_tokens=body.included_tokens,
        booking_window_days=body.booking_window_days,
        max_simultaneous_bookings=body.max_simultaneous_bookings,
        notes=body.notes,
    )
    session.add(row)
    try:
        session.flush()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail={"code": "duplicate_tier", "message": "A tier with that name already exists."},
        ) from None
    session.refresh(row)
    return TierOut.model_validate(row)


@router.patch("/tiers/{name}", response_model=TierOut)
def patch_tier(name: str, body: TierPatch, session: DbSession, _owner: Owner) -> TierOut:
    row = session.get(MembershipTier, name.strip().lower())
    if row is None:
        raise HTTPException(status_code=404, detail={"code": "not_found", "message": "Tier not found."})
    updates = body.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(row, key, value)
    session.add(row)
    session.flush()
    session.refresh(row)
    return TierOut.model_validate(row)
