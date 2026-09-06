from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, ValidationError, field_validator

from app.models import (
    BookingKind,
    BookingStatus,
    HoistStatus,
    MemberStatus,
    NotificationChannel,
    NotificationStatus,
    TokenTransactionKind,
)


def _blank_to_none(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


class WaitlistCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=40)
    notes: str | None = Field(default=None, max_length=2000)

    @field_validator("name")
    @classmethod
    def strip_name(cls, value: str) -> str:
        return value.strip()

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return str(value).strip().lower()

    @field_validator("phone", "notes", mode="before")
    @classmethod
    def empty_optional(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return _blank_to_none(str(value))


class WaitlistEntryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    email: EmailStr
    phone: str | None
    notes: str | None
    contacted_at: datetime | None
    created_at: datetime


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return str(value).strip().lower()


class PrincipalOut(BaseModel):
    role: str
    email: str
    member_id: UUID | None = None


class TierOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    display_name: str
    price: Decimal
    included_tokens: int
    booking_window_days: int
    max_simultaneous_bookings: int
    notes: str | None
    created_at: datetime
    updated_at: datetime


class TierCreate(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    display_name: str = Field(min_length=1, max_length=120)
    price: Decimal = Field(ge=0)
    included_tokens: int = Field(ge=0)
    booking_window_days: int = Field(ge=1)
    max_simultaneous_bookings: int = Field(ge=1)
    notes: str | None = None

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        return value.strip().lower()

    @field_validator("display_name")
    @classmethod
    def strip_display(cls, value: str) -> str:
        return value.strip()


class TierPatch(BaseModel):
    display_name: str | None = Field(default=None, min_length=1, max_length=120)
    price: Decimal | None = Field(default=None, ge=0)
    included_tokens: int | None = Field(default=None, ge=0)
    booking_window_days: int | None = Field(default=None, ge=1)
    max_simultaneous_bookings: int | None = Field(default=None, ge=1)
    notes: str | None = None


class MemberOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    email: EmailStr
    phone: str | None
    tier_name: str
    status: MemberStatus
    waiver_signed_at: datetime | None
    waiver_version: str | None
    emergency_contact_name: str | None
    emergency_contact_phone: str | None
    token_balance: Decimal
    deposit_balance: Decimal
    created_at: datetime
    updated_at: datetime


class MemberCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=40)
    tier_name: str = Field(min_length=1, max_length=64)
    status: MemberStatus = MemberStatus.ACTIVE
    waiver_signed_at: datetime | None = None
    waiver_version: str | None = Field(default=None, max_length=64)
    emergency_contact_name: str | None = Field(default=None, max_length=200)
    emergency_contact_phone: str | None = Field(default=None, max_length=40)
    allocate_tokens: bool = True

    @field_validator("name")
    @classmethod
    def strip_name(cls, value: str) -> str:
        return value.strip()

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return str(value).strip().lower()

    @field_validator("tier_name")
    @classmethod
    def normalize_tier(cls, value: str) -> str:
        return value.strip().lower()

    @field_validator("phone", "waiver_version", "emergency_contact_name", "emergency_contact_phone", mode="before")
    @classmethod
    def empty_optional(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return _blank_to_none(str(value))


class MemberPatch(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    phone: str | None = Field(default=None, max_length=40)
    tier_name: str | None = Field(default=None, min_length=1, max_length=64)
    status: MemberStatus | None = None
    waiver_signed_at: datetime | None = None
    waiver_version: str | None = Field(default=None, max_length=64)
    emergency_contact_name: str | None = Field(default=None, max_length=200)
    emergency_contact_phone: str | None = Field(default=None, max_length=40)


class TokenAdjustment(BaseModel):
    amount: Decimal
    note: str | None = Field(default=None, max_length=2000)


class TokenTransactionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    member_id: UUID
    booking_id: UUID | None
    kind: TokenTransactionKind
    amount: Decimal
    note: str | None
    meta: dict | None = None
    created_at: datetime


class HoistOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    location_label: str
    status: HoistStatus
    is_shop: bool
    created_at: datetime
    updated_at: datetime


class HoistCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    location_label: str = Field(default="", max_length=120)
    status: HoistStatus = HoistStatus.AVAILABLE
    is_shop: bool = False

    @field_validator("name", "location_label")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip()


class HoistPatch(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    location_label: str | None = Field(default=None, max_length=120)
    status: HoistStatus | None = None
    is_shop: bool | None = None


class PricingRuleOut(BaseModel):
    band_id: str
    band_label: str
    band_multiplier: str
    overlay_id: str
    overlay_label: str
    advance_multiplier: str
    fill_id: str = "none"
    fill_label: str = "No fill"
    fill_multiplier: str = "1"
    fill_discount_pct: str = "0"
    hours: str
    base_tokens: str
    final_reserve_cost: str
    tz: str


class BookingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    member_id: UUID | None
    member_name: str
    hoist_id: UUID
    hoist_name: str
    kind: BookingKind
    start_at: datetime
    end_at: datetime
    status: BookingStatus
    reserved_tokens: Decimal
    pricing_rule: PricingRuleOut | None = None
    notes: str | None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_booking(cls, booking) -> BookingOut:
        hoist = getattr(booking, "hoist", None)
        member = getattr(booking, "member", None)
        raw = booking.pricing_rule
        rule = None
        if raw:
            try:
                rule = PricingRuleOut.model_validate(raw)
            except ValidationError:
                rule = None
        return cls(
            id=booking.id,
            member_id=booking.member_id,
            member_name=member.name if member is not None else "Shop",
            hoist_id=booking.hoist_id,
            hoist_name=hoist.name if hoist is not None else "Unknown hoist",
            kind=booking.kind,
            start_at=booking.start_at,
            end_at=booking.end_at,
            status=booking.status,
            reserved_tokens=booking.reserved_tokens,
            pricing_rule=rule,
            notes=booking.notes,
            created_at=booking.created_at,
            updated_at=booking.updated_at,
        )


class BookingCreate(BaseModel):
    member_id: UUID | None = None
    hoist_id: UUID
    start_at: datetime
    end_at: datetime
    kind: BookingKind = BookingKind.CUSTOMER
    tokens: Decimal | None = Field(default=None, description="Ignored. Server computes reserve from duration.")
    notes: str | None = Field(default=None, max_length=2000)


class BookingQuoteRequest(BaseModel):
    start_at: datetime
    end_at: datetime
    member_id: UUID | None = None
    tokens: Decimal | None = Field(default=None, description="Ignored display hint.")


class BookingQuoteOut(BaseModel):
    pricing_rule: PricingRuleOut
    reserved_tokens: Decimal
    token_balance: Decimal | None = None
    token_balance_after: Decimal | None = None


class BookingComplete(BaseModel):
    unused_tokens: Decimal = Field(default=Decimal("0"), ge=0)


class MemberBookingCreate(BaseModel):
    hoist_id: UUID
    start_at: datetime
    end_at: datetime
    tokens: Decimal | None = Field(default=None, description="Ignored. Server computes reserve from duration.")
    notes: str | None = Field(default=None, max_length=2000)


class MemberBookingQuoteRequest(BaseModel):
    start_at: datetime
    end_at: datetime
    tokens: Decimal | None = Field(default=None, description="Ignored display hint.")


class MemberSelfOut(MemberOut):
    booking_window_days: int
    max_simultaneous_bookings: int
    included_tokens: int
    bookings: list[BookingOut]
    tokens: list[TokenTransactionOut]


class OccupancyOut(BaseModel):
    booking_id: UUID
    hoist_id: UUID
    hoist_name: str
    start_at: datetime
    end_at: datetime
    status: BookingStatus
    own: bool


class MemberScheduleOut(BaseModel):
    hoists: list[HoistOut]
    bookings: list[BookingOut]
    occupancy: list[OccupancyOut]


class MemberDetailOut(MemberOut):
    bookings: list[BookingOut]


class MemberAtRiskOut(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    tier_name: str
    token_balance: Decimal


class HoistSnapshotOut(HoistOut):
    current_booking: BookingOut | None = None


class DashboardOut(BaseModel):
    hoists: list[HoistSnapshotOut]
    today_bookings: list[BookingOut]
    waitlist_count: int
    token_at_risk: list[MemberAtRiskOut]


class FillGapOut(BaseModel):
    hoist_id: UUID
    hoist_name: str
    start_at: datetime
    end_at: datetime
    hours: Decimal


class FillPreviewOut(BaseModel):
    target_date: str
    tz: str
    window_start: datetime
    window_end: datetime
    bay_count: int
    capacity_hours: Decimal
    booked_hours: Decimal
    open_hours: Decimal
    open_ratio: Decimal
    discount_pct: Decimal
    fill_multiplier: Decimal
    urgency: str
    applies: bool
    gaps: list[FillGapOut]
    offer_id: UUID | None = None
    source: str = "none"

    @classmethod
    def from_snapshot(cls, snapshot) -> FillPreviewOut:
        return cls(
            target_date=snapshot.target_date.isoformat(),
            tz=snapshot.tz,
            window_start=snapshot.window_start,
            window_end=snapshot.window_end,
            bay_count=snapshot.bay_count,
            capacity_hours=snapshot.capacity_hours,
            booked_hours=snapshot.booked_hours,
            open_hours=snapshot.open_hours,
            open_ratio=snapshot.open_ratio,
            discount_pct=snapshot.discount_pct,
            fill_multiplier=snapshot.fill_multiplier,
            urgency=snapshot.urgency,
            applies=snapshot.applies,
            gaps=[
                FillGapOut(
                    hoist_id=gap.hoist_id,
                    hoist_name=gap.hoist_name,
                    start_at=gap.start_at,
                    end_at=gap.end_at,
                    hours=gap.hours,
                )
                for gap in snapshot.gaps
            ],
            offer_id=snapshot.offer_id,
            source=snapshot.source,
        )


class FillNotifyRequest(BaseModel):
    dry_run: bool = True
    discount_pct: Decimal | None = Field(default=None, ge=0, le=100)
    channels: list[str] = Field(default_factory=lambda: ["email"])


class NotificationOutboxOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    channel: NotificationChannel
    member_id: UUID | None
    fill_offer_id: UUID | None
    to_address: str | None
    subject: str | None
    body: str | None
    payload: dict | None = None
    status: NotificationStatus
    attempts: int
    last_error: str | None
    dry_run: bool
    sent_at: datetime | None
    created_at: datetime


class FillNotifyOut(BaseModel):
    preview: FillPreviewOut
    dry_run: bool
    published: bool
    queued: int
    notifications: list[NotificationOutboxOut]
