from __future__ import annotations

from decimal import Decimal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.deps import DbSession, Owner
from app.models import MembershipTier, PricingBand, PricingOverlay
from app.schemas import TierCreate, TierOut, TierPatch
from app.services.pricing import PricingError, ensure_pricing_settings, quantize_multiplier

router = APIRouter(tags=["tiers"])


class PricingMultiplierOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    label: str
    multiplier: Decimal
    sort_order: int


class PricingSettingsOut(BaseModel):
    bands: list[PricingMultiplierOut]
    overlays: list[PricingMultiplierOut]


class MultiplierPatch(BaseModel):
    multiplier: Decimal = Field(gt=0, le=Decimal("9999.9999"))


def _multiplier_or_422(value: Decimal) -> Decimal:
    try:
        return quantize_multiplier(value)
    except PricingError as exc:
        raise HTTPException(
            status_code=422,
            detail={"code": exc.code, "message": exc.message},
        ) from exc


@router.get("/tiers/pricing", response_model=PricingSettingsOut)
def list_pricing_settings(session: DbSession, _owner: Owner) -> PricingSettingsOut:
    ensure_pricing_settings(session)
    bands = session.scalars(select(PricingBand).order_by(PricingBand.sort_order, PricingBand.id)).all()
    overlays = session.scalars(
        select(PricingOverlay).order_by(PricingOverlay.sort_order, PricingOverlay.id)
    ).all()
    return PricingSettingsOut(
        bands=[PricingMultiplierOut.model_validate(row) for row in bands],
        overlays=[PricingMultiplierOut.model_validate(row) for row in overlays],
    )


@router.patch("/tiers/bands/{band_id}", response_model=PricingMultiplierOut)
def patch_band_multiplier(
    band_id: str,
    body: MultiplierPatch,
    session: DbSession,
    _owner: Owner,
) -> PricingMultiplierOut:
    ensure_pricing_settings(session)
    row = session.get(PricingBand, band_id)
    if row is None:
        raise HTTPException(
            status_code=404,
            detail={"code": "not_found", "message": "Band not found."},
        )
    row.multiplier = _multiplier_or_422(body.multiplier)
    session.add(row)
    session.flush()
    session.refresh(row)
    return PricingMultiplierOut.model_validate(row)


@router.patch("/tiers/overlays/{overlay_id}", response_model=PricingMultiplierOut)
def patch_overlay_multiplier(
    overlay_id: str,
    body: MultiplierPatch,
    session: DbSession,
    _owner: Owner,
) -> PricingMultiplierOut:
    ensure_pricing_settings(session)
    row = session.get(PricingOverlay, overlay_id)
    if row is None:
        raise HTTPException(
            status_code=404,
            detail={"code": "not_found", "message": "Overlay not found."},
        )
    row.multiplier = _multiplier_or_422(body.multiplier)
    session.add(row)
    session.flush()
    session.refresh(row)
    return PricingMultiplierOut.model_validate(row)


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
