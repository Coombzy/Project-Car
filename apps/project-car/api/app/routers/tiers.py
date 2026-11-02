from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.deps import DbSession, Owner
from app.models import MembershipTier, PricingBand, PricingOverlay
from app.schemas import MemberRateChartOut, PlanOfferOut, TierCreate, TierOut, TierPatch
from app.services.peak_cap import PEAK_BAND_IDS, PEAK_HOURS_PER_WEEK
from app.services.pricing import PricingError, ensure_pricing_settings, quantize_multiplier, weekly_rate_chart
from app.services.staff import reject_ai
from app.services.tokens import grant_period_allocations

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


class PricingMultiplierUpdate(BaseModel):
    id: str = Field(min_length=1, max_length=64)
    multiplier: Decimal = Field(gt=0, le=Decimal("9999.9999"))


class PricingSettingsPatch(BaseModel):
    bands: list[PricingMultiplierUpdate] = Field(default_factory=list)
    overlays: list[PricingMultiplierUpdate] = Field(default_factory=list)


class PeriodAllocationGrantOut(BaseModel):
    member_id: UUID
    tier_name: str
    amount: Decimal


class PeriodAllocationOut(BaseModel):
    period: str
    tz: str
    granted: list[PeriodAllocationGrantOut]
    skipped: int


def _multiplier_or_422(value: Decimal) -> Decimal:
    try:
        return quantize_multiplier(value)
    except PricingError as exc:
        raise HTTPException(
            status_code=422,
            detail={"code": exc.code, "message": exc.message},
        ) from exc


def _collect_multiplier_writes(
    session: Session,
    model: type[PricingBand] | type[PricingOverlay],
    updates: list[PricingMultiplierUpdate],
    missing: str,
) -> list[tuple[PricingBand | PricingOverlay, Decimal]]:
    """Resolve every id and multiplier. Nothing is assigned until this returns."""
    pending: list[tuple[PricingBand | PricingOverlay, Decimal]] = []
    seen: set[str] = set()
    for item in updates:
        if item.id in seen:
            raise HTTPException(
                status_code=422,
                detail={
                    "code": "validation_error",
                    "message": "Each multiplier can be set once.",
                },
            )
        seen.add(item.id)
        row = session.get(model, item.id)
        if row is None:
            raise HTTPException(
                status_code=404,
                detail={"code": "not_found", "message": missing},
            )
        pending.append((row, _multiplier_or_422(item.multiplier)))
    return pending


@router.get("/tiers/rate-chart", response_model=MemberRateChartOut)
def owner_rate_chart(session: DbSession, _owner: Owner) -> MemberRateChartOut:
    """Same saved-band week the member chart, quote, and peak cap use."""
    return MemberRateChartOut.model_validate(
        weekly_rate_chart(
            session,
            peak_band_ids=PEAK_BAND_IDS,
            peak_cap_hours=PEAK_HOURS_PER_WEEK,
        )
    )


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


@router.patch("/tiers/pricing", response_model=PricingSettingsOut)
def patch_pricing_settings(
    body: PricingSettingsPatch,
    session: DbSession,
    _owner: Owner,
) -> PricingSettingsOut:
    """Validate every submitted multiplier, then write them in this request's transaction."""
    ensure_pricing_settings(session)
    pending = [
        *_collect_multiplier_writes(session, PricingBand, body.bands, "Band not found."),
        *_collect_multiplier_writes(session, PricingOverlay, body.overlays, "Overlay not found."),
    ]
    for row, multiplier in pending:
        row.multiplier = multiplier
        session.add(row)
    if pending:
        session.flush()
    return list_pricing_settings(session, _owner)


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


@router.get("/plans", response_model=list[PlanOfferOut])
def list_plans(session: DbSession) -> list[PlanOfferOut]:
    """Signup reads the same rows the owner edits. No session required."""
    rows = session.scalars(select(MembershipTier).order_by(MembershipTier.name)).all()
    return [PlanOfferOut.model_validate(row) for row in rows]


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
    # These columns are NOT NULL. An explicit null is not a clear.
    # Writing None flushed IntegrityError out of the route (500).
    blocked = [
        field
        for field in (
            "display_name",
            "price",
            "included_tokens",
            "booking_window_days",
            "max_simultaneous_bookings",
        )
        if field in updates and updates[field] is None
    ]
    if blocked:
        raise HTTPException(
            status_code=422,
            detail={
                "code": "validation_error",
                "message": f"{', '.join(blocked)} cannot be null.",
            },
        )
    for key, value in updates.items():
        setattr(row, key, value)
    session.add(row)
    session.flush()
    session.refresh(row)
    return TierOut.model_validate(row)


@router.post("/tiers/period-allocation/grant", response_model=PeriodAllocationOut)
def grant_period_allocation(session: DbSession, owner: Owner) -> PeriodAllocationOut:
    """Owner button. One monthly_allocation per active member per Regina month.

    The extra path segment keeps this off PATCH /tiers/{name}, which would
    answer POST /tiers/period-allocation with 405.

    A second call in the same month inserts nothing. There is no scheduler.
    """
    reject_ai(
        owner,
        code="allocation_requires_human",
        message="An AI cannot grant a period allotment on its own.",
    )
    result = grant_period_allocations(session)
    return PeriodAllocationOut(
        period=result.period,
        tz=result.tz,
        granted=[
            PeriodAllocationGrantOut(member_id=row.member_id, tier_name=row.tier_name, amount=row.amount)
            for row in result.granted
        ],
        skipped=result.skipped,
    )
