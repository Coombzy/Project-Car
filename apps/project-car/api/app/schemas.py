from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, ValidationError, computed_field, field_validator

from app.models import (
    ActorKind,
    BookingKind,
    BookingStatus,
    ChatSenderRole,
    DraftKind,
    DraftStatus,
    HoistStatus,
    JobEvent,
    JobEventKind,
    MemberStatus,
    NotificationChannel,
    NotificationStatus,
    PartsOrderStatus,
    PartsRequest,
    PartsRequestStatus,
    ShopHoistRequestStatus,
    ShopJobStatus,
    TodoStatus,
    TokenTransactionKind,
    ToolCribEvent,
    ToolCribEventKind,
)
from app.services.plan_price import (
    PLAN_CURRENCY,
    PLAN_PERIOD,
    gst_on,
    price_mark as stored_price_mark,
    total_with_gst,
)
from app.services.tokens import GST_RATE


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

    @field_validator("name", mode="before")
    @classmethod
    def blank_name(cls, value: object) -> object:
        # Whitespace-only becomes "" before min_length. Other values stay raw so max_length is unchanged.
        if isinstance(value, str) and not value.strip():
            return ""
        return value

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
    member_id: UUID | None = None
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


class PlanPriceOut(BaseModel):
    """Monthly CAD price from the tier row, plus GST from the stored rate."""

    model_config = ConfigDict(from_attributes=True)

    price: Decimal
    notes: str | None = None

    @computed_field
    @property
    def currency(self) -> str:
        return PLAN_CURRENCY

    @computed_field
    @property
    def billing_period(self) -> str:
        return PLAN_PERIOD

    @computed_field
    @property
    def gst_rate(self) -> Decimal:
        return GST_RATE

    @computed_field
    @property
    def gst_cad(self) -> Decimal:
        return gst_on(self.price)

    @computed_field
    @property
    def total_cad(self) -> Decimal:
        return total_with_gst(self.price)

    @computed_field
    @property
    def price_mark(self) -> str | None:
        return stored_price_mark(self.notes)


class PlanOfferOut(PlanPriceOut):
    """Signup payload. The price is the saved tier row, not a copy in the page."""

    name: str
    display_name: str
    included_tokens: int


class TierOut(PlanPriceOut):
    name: str
    display_name: str
    included_tokens: int
    booking_window_days: int
    max_simultaneous_bookings: int
    created_at: datetime
    updated_at: datetime


# Stand-in caps until Ben locks real ones. Two decimal places, and small enough
# that Postgres Numeric(10, 2) and the integer columns cannot overflow.
_TIER_PRICE_MAX = Decimal("9999.99")
_TIER_INCLUDED_TOKENS_MAX = 100_000
_TIER_BOOKING_WINDOW_DAYS_MAX = 365
_TIER_MAX_SIMULTANEOUS_BOOKINGS_MAX = 20


class TierCreate(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    display_name: str = Field(min_length=1, max_length=120)
    price: Decimal = Field(ge=0, le=_TIER_PRICE_MAX, max_digits=6, decimal_places=2)
    included_tokens: int = Field(ge=0, le=_TIER_INCLUDED_TOKENS_MAX)
    booking_window_days: int = Field(ge=1, le=_TIER_BOOKING_WINDOW_DAYS_MAX)
    max_simultaneous_bookings: int = Field(ge=1, le=_TIER_MAX_SIMULTANEOUS_BOOKINGS_MAX)
    notes: str | None = None

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        return value.strip().lower()

    @field_validator("display_name", mode="before")
    @classmethod
    def blank_display(cls, value: object) -> object:
        # Whitespace-only becomes "" before min_length. Other values stay raw so max_length is unchanged.
        if isinstance(value, str) and not value.strip():
            return ""
        return value

    @field_validator("display_name")
    @classmethod
    def strip_display(cls, value: str) -> str:
        return value.strip()


class TierPatch(BaseModel):
    display_name: str | None = Field(default=None, min_length=1, max_length=120)
    price: Decimal | None = Field(
        default=None, ge=0, le=_TIER_PRICE_MAX, max_digits=6, decimal_places=2
    )
    included_tokens: int | None = Field(default=None, ge=0, le=_TIER_INCLUDED_TOKENS_MAX)
    booking_window_days: int | None = Field(default=None, ge=1, le=_TIER_BOOKING_WINDOW_DAYS_MAX)
    max_simultaneous_bookings: int | None = Field(
        default=None, ge=1, le=_TIER_MAX_SIMULTANEOUS_BOOKINGS_MAX
    )
    notes: str | None = None

    @field_validator("display_name", mode="before")
    @classmethod
    def blank_display(cls, value: object) -> object:
        # Whitespace-only becomes "" before min_length. Other values stay raw so max_length is unchanged.
        if isinstance(value, str) and not value.strip():
            return ""
        return value

    @field_validator("display_name")
    @classmethod
    def strip_display(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip()


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
    allowance_balance: Decimal
    purchased_balance: Decimal
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

    @field_validator("name", mode="before")
    @classmethod
    def blank_name(cls, value: object) -> object:
        # Whitespace-only becomes "" before min_length. Other values stay raw so max_length is unchanged.
        if isinstance(value, str) and not value.strip():
            return ""
        return value

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


class MemberPasswordSet(BaseModel):
    password: str = Field(min_length=1, max_length=200)


class MemberPatch(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    phone: str | None = Field(default=None, max_length=40)
    tier_name: str | None = Field(default=None, min_length=1, max_length=64)
    status: MemberStatus | None = None
    waiver_signed_at: datetime | None = None
    waiver_version: str | None = Field(default=None, max_length=64)
    emergency_contact_name: str | None = Field(default=None, max_length=200)
    emergency_contact_phone: str | None = Field(default=None, max_length=40)

    @field_validator("name", mode="before")
    @classmethod
    def blank_name(cls, value: object) -> object:
        # Whitespace-only becomes "" before min_length. Other values stay raw so max_length is unchanged.
        if isinstance(value, str) and not value.strip():
            return ""
        return value

    @field_validator("name")
    @classmethod
    def strip_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip()


class TokenAdjustment(BaseModel):
    amount: Decimal
    # Required; checked in the router so a missing reason is 422 reason_required.
    reason: str | None = None
    note: str | None = Field(default=None, max_length=2000)


class DepositCreate(BaseModel):
    action: Literal["take", "return", "keep"]
    amount: Decimal = Field(gt=0, decimal_places=2)
    payment_id: str = Field(min_length=1, max_length=120)
    note: str | None = Field(default=None, max_length=2000)

    @field_validator("payment_id")
    @classmethod
    def strip_payment_id(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("payment id is required")
        return stripped


class DollarChargeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    purpose: str
    payment_id: str | None
    subtotal_cad: Decimal
    gst_cad: Decimal
    total_cad: Decimal
    gst_rate: Decimal
    created_at: datetime


class TokenPurchaseCreate(BaseModel):
    """A PayPal payment the Owner has seen land. Tokens and CAD come from that payment."""

    payment_id: str = Field(min_length=1, max_length=120)
    tokens: Decimal = Field(gt=0, decimal_places=2)
    subtotal_cad: Decimal = Field(ge=0, decimal_places=2)
    note: str | None = Field(default=None, max_length=2000)

    @field_validator("payment_id")
    @classmethod
    def strip_payment_id(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("payment_id cannot be blank.")
        return stripped


class TokenTransactionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    member_id: UUID
    booking_id: UUID | None
    kind: TokenTransactionKind
    amount: Decimal
    allowance_amount: Decimal
    purchased_amount: Decimal
    note: str | None
    meta: dict | None = None
    payment_ref: str | None = None
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

    @field_validator("name", mode="before")
    @classmethod
    def blank_name(cls, value: object) -> object:
        # Whitespace-only becomes "" before min_length. Other values stay raw so max_length is unchanged.
        if isinstance(value, str) and not value.strip():
            return ""
        return value

    @field_validator("name", "location_label")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip()


class HoistPatch(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    location_label: str | None = Field(default=None, max_length=120)
    status: HoistStatus | None = None
    is_shop: bool | None = None
    # Closing a bay (maintenance / locked) with future bookings needs both.
    cancel_bookings: bool = False
    reason: str | None = None

    @field_validator("name", mode="before")
    @classmethod
    def blank_name(cls, value: object) -> object:
        # Whitespace-only becomes "" before min_length. Other values stay raw so max_length is unchanged.
        if isinstance(value, str) and not value.strip():
            return ""
        return value

    @field_validator("name")
    @classmethod
    def strip_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip()


class MemberRateBandOut(BaseModel):
    id: str
    label: str
    multiplier: str
    tokens_per_hour: str


class MemberRateHourOut(BaseModel):
    weekday: int
    day_label: str
    hour: int
    band_id: str
    label: str
    tokens_per_hour: str
    counts_toward_peak_cap: bool


class MemberRateChartOut(BaseModel):
    tz_label: str
    peak_cap_hours: int
    note: str
    bands: list[MemberRateBandOut]
    hours: list[MemberRateHourOut]


class PricingSegmentOut(BaseModel):
    start_at: datetime
    end_at: datetime
    band_id: str
    band_label: str
    band_multiplier: str
    band_tokens: str


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
    # Older bookings were priced from the start band and carry no segments.
    banded_tokens: str | None = None
    final_reserve_cost: str
    tz: str
    segments: list[PricingSegmentOut] = []


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
    hoist_id: UUID | None = None
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


class BookingCancel(BaseModel):
    """Owner cancel. A written reason is required when the cancel refunds."""

    reason: str | None = None


class BookingComplete(BaseModel):
    # Only 0 is accepted: unused time is never refunded once a visit has
    # started (Ben, D16). The Owner web form still posts 0.
    unused_tokens: Decimal = Field(default=Decimal("0"), ge=0)


class MemberBookingCreate(BaseModel):
    hoist_id: UUID | None = None
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


class BookedHourOut(BaseModel):
    booking_id: UUID
    hoist_id: UUID
    hoist_name: str
    kind: BookingKind
    status: BookingStatus
    hour_start: datetime
    hour_end: datetime
    member_id: UUID | None
    member_name: str
    vehicle_label: str
    notes: str | None


class HoistSnapshotOut(HoistOut):
    current_booking: BookingOut | None = None
    next_hours: list[BookedHourOut] = Field(default_factory=list)


class TodoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    owner_email: str | None
    member_id: UUID | None
    title: str
    notes: str | None
    due_at: datetime | None
    status: TodoStatus
    created_at: datetime
    updated_at: datetime


class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    notes: str | None = Field(default=None, max_length=2000)
    due_at: datetime | None = None

    @field_validator("title", mode="before")
    @classmethod
    def blank_title(cls, value: object) -> object:
        # Whitespace-only becomes "" before min_length. Other values stay raw so max_length is unchanged.
        if isinstance(value, str) and not value.strip():
            return ""
        return value

    @field_validator("title")
    @classmethod
    def strip_title(cls, value: str) -> str:
        return value.strip()

    @field_validator("notes", mode="before")
    @classmethod
    def empty_notes(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return _blank_to_none(str(value))


class TodoPatch(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    notes: str | None = Field(default=None, max_length=2000)
    due_at: datetime | None = None
    clear_due: bool = False
    status: TodoStatus | None = None

    @field_validator("title", mode="before")
    @classmethod
    def blank_title(cls, value: object) -> object:
        # Whitespace-only becomes "" before min_length. Other values stay raw so max_length is unchanged.
        if isinstance(value, str) and not value.strip():
            return ""
        return value


class PartsOrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    po_number: str
    sku: str | None
    what: str
    vendor: str
    for_label: str
    status: PartsOrderStatus
    ordered_at: datetime
    shipped_at: datetime | None
    eta_at: datetime | None
    received_at: datetime | None
    tracking: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime


class PartsRequestOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    member_id: UUID
    member_name: str | None = None
    sku: str
    note: str | None
    status: PartsRequestStatus
    created_at: datetime

    @classmethod
    def from_row(cls, row: PartsRequest) -> PartsRequestOut:
        name = row.member.name if row.member is not None else None
        return cls.model_validate(row).model_copy(update={"member_name": name})


class PartsOrderPatch(BaseModel):
    status: PartsOrderStatus


class PartsRequestPatch(BaseModel):
    status: PartsRequestStatus


class PartsRequestCreate(BaseModel):
    sku: str = Field(min_length=1, max_length=80)
    note: str | None = Field(default=None, max_length=2000)

    @field_validator("sku", mode="before")
    @classmethod
    def blank_sku(cls, value: object) -> object:
        # Whitespace-only becomes "" before min_length. Other values stay raw so max_length is unchanged.
        if isinstance(value, str) and not value.strip():
            return ""
        return value

    @field_validator("sku")
    @classmethod
    def strip_sku(cls, value: str) -> str:
        return value.strip()

    @field_validator("note", mode="before")
    @classmethod
    def empty_note(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return _blank_to_none(str(value))


class CalendarProviderStatusOut(BaseModel):
    connected: bool
    status: str
    ready: bool
    label: str
    hint: str | None = None


class CalendarStatusOut(BaseModel):
    google: CalendarProviderStatusOut
    apple: CalendarProviderStatusOut
    next: str


class DashboardOut(BaseModel):
    tz: str
    window_start: datetime
    window_end: datetime
    hoists: list[HoistSnapshotOut]
    today_bookings: list[BookingOut]
    waitlist_count: int
    token_at_risk: list[MemberAtRiskOut]
    todos: list[TodoOut] = Field(default_factory=list)
    parts_orders: list[PartsOrderOut] = Field(default_factory=list)
    calendar: CalendarStatusOut | None = None


class MemberDashboardOut(BaseModel):
    tz: str
    window_start: datetime
    window_end: datetime
    hoists: list[HoistSnapshotOut]
    todos: list[TodoOut]
    calendar: CalendarStatusOut


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


class ChatParticipantOut(BaseModel):
    member_id: UUID
    name: str
    email: str


class ChatMessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    room_id: UUID
    sender_role: ChatSenderRole
    sender_member_id: UUID | None
    sender_email: str
    sender_name: str
    body: str
    created_at: datetime


class ChatRoomOut(BaseModel):
    id: UUID
    title: str
    muted: bool
    created_by_email: str
    created_at: datetime
    updated_at: datetime
    participants: list[ChatParticipantOut]
    last_message: ChatMessageOut | None = None
    last_message_at: datetime | None = None

    @classmethod
    def from_room(cls, room, last=None) -> ChatRoomOut:
        participants = []
        for row in sorted(room.participants, key=lambda item: (item.member.name if item.member else "")):
            if row.member is None:
                continue
            participants.append(
                ChatParticipantOut(
                    member_id=row.member_id,
                    name=row.member.name,
                    email=row.member.email,
                )
            )
        last_out = ChatMessageOut.model_validate(last) if last is not None else None
        return cls(
            id=room.id,
            title=room.title,
            muted=room.muted,
            created_by_email=room.created_by_email,
            created_at=room.created_at,
            updated_at=room.updated_at,
            participants=participants,
            last_message=last_out,
            last_message_at=last.created_at if last is not None else None,
        )


class ChatRoomCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    member_ids: list[UUID] = Field(min_length=1)

    @field_validator("title", mode="before")
    @classmethod
    def blank_title(cls, value: object) -> object:
        # Whitespace-only becomes "" before min_length. Other values stay raw so max_length is unchanged.
        if isinstance(value, str) and not value.strip():
            return ""
        return value

    @field_validator("title")
    @classmethod
    def strip_title(cls, value: str) -> str:
        return value.strip()


class ChatMessageCreate(BaseModel):
    body: str = Field(min_length=1, max_length=4000)

    @field_validator("body", mode="before")
    @classmethod
    def blank_body(cls, value: object) -> object:
        # Whitespace-only becomes "" before min_length. Other values stay raw so max_length is unchanged.
        if isinstance(value, str) and not value.strip():
            return ""
        return value

    @field_validator("body")
    @classmethod
    def strip_body(cls, value: str) -> str:
        return value.strip()


class ChatMuteRequest(BaseModel):
    muted: bool


class ToolCribEventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    member_id: UUID
    member_name: str | None = None
    sku: str
    kind: ToolCribEventKind
    note: str | None
    checkout_id: UUID | None
    created_at: datetime

    @classmethod
    def from_row(cls, row: ToolCribEvent) -> ToolCribEventOut:
        name = row.member.name if row.member is not None else None
        return cls.model_validate(row).model_copy(update={"member_name": name})


class ToolCribCheckoutCreate(BaseModel):
    member_id: UUID
    sku: str = Field(min_length=1, max_length=80)
    note: str | None = Field(default=None, max_length=2000)

    @field_validator("sku", mode="before")
    @classmethod
    def blank_sku(cls, value: object) -> object:
        # Whitespace-only becomes "" before min_length. Other values stay raw so max_length is unchanged.
        if isinstance(value, str) and not value.strip():
            return ""
        return value

    @field_validator("sku")
    @classmethod
    def strip_sku(cls, value: str) -> str:
        return value.strip()

    @field_validator("note", mode="before")
    @classmethod
    def empty_note(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return _blank_to_none(str(value))


class ToolCribReturnCreate(BaseModel):
    sku: str = Field(min_length=1, max_length=80)
    note: str | None = Field(default=None, max_length=2000)

    @field_validator("sku", mode="before")
    @classmethod
    def blank_sku(cls, value: object) -> object:
        # Whitespace-only becomes "" before min_length. Other values stay raw so max_length is unchanged.
        if isinstance(value, str) and not value.strip():
            return ""
        return value

    @field_validator("sku")
    @classmethod
    def strip_sku(cls, value: str) -> str:
        return value.strip()

    @field_validator("note", mode="before")
    @classmethod
    def empty_note(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return _blank_to_none(str(value))


class ChatMessagePage(BaseModel):
    messages: list[ChatMessageOut]
    cursor: UUID | None = None


class ShopHoistRequestOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    record: Literal["shop_hoist_request"] = "shop_hoist_request"
    id: UUID
    member_id: UUID
    member_name: str
    hoist_id: UUID
    hoist_name: str
    start_at: datetime
    end_at: datetime
    status: ShopHoistRequestStatus
    token_quote: Decimal
    pricing_rule: PricingRuleOut | None = None
    notes: str | None
    created_by_kind: ActorKind
    created_by_id: str
    booking_id: UUID | None = None
    decided_by_kind: ActorKind | None = None
    decided_by_id: str | None = None
    decided_at: datetime | None = None
    created_at: datetime

    @classmethod
    def from_row(cls, row) -> ShopHoistRequestOut:
        hoist = getattr(row, "hoist", None)
        member = getattr(row, "member", None)
        raw = row.pricing_rule
        rule = None
        if raw:
            try:
                rule = PricingRuleOut.model_validate(raw)
            except ValidationError:
                rule = None
        return cls(
            record="shop_hoist_request",
            id=row.id,
            member_id=row.member_id,
            member_name=member.name if member is not None else "Member",
            hoist_id=row.hoist_id,
            hoist_name=hoist.name if hoist is not None else "Shop hoist",
            start_at=row.start_at,
            end_at=row.end_at,
            status=row.status,
            token_quote=row.token_quote,
            pricing_rule=rule,
            notes=row.notes,
            created_by_kind=row.created_by_kind,
            created_by_id=row.created_by_id,
            booking_id=row.booking_id,
            decided_by_kind=row.decided_by_kind,
            decided_by_id=row.decided_by_id,
            decided_at=row.decided_at,
            created_at=row.created_at,
        )


class StaffDecisionOut(BaseModel):
    request_id: UUID
    status: str
    actor_kind: ActorKind
    actor_id: str
    action_id: UUID
    action: str
    booking_id: UUID | None = None
    token_balance: Decimal | None = None


class StaffPartsRequestCreate(BaseModel):
    member_id: UUID | None = None
    sku: str = Field(min_length=1, max_length=80)
    note: str | None = Field(default=None, max_length=2000)

    @field_validator("sku", mode="before")
    @classmethod
    def strip_sku(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip()
        return value

    @field_validator("note", mode="before")
    @classmethod
    def empty_note(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if not isinstance(value, str):
            return value
        return _blank_to_none(value)


class StaffPartsRequestOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    member_id: UUID
    sku: str
    note: str | None
    status: ShopHoistRequestStatus
    created_by_kind: ActorKind
    created_by_id: str
    decided_by_kind: ActorKind | None = None
    decided_by_id: str | None = None


class ToolCribExceptionCreate(BaseModel):
    member_id: UUID | None = None
    tool_code: str = Field(min_length=1, max_length=80)
    reason: str | None = Field(default=None, max_length=2000)

    @field_validator("tool_code", mode="before")
    @classmethod
    def strip_tool_code(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip()
        return value

    @field_validator("reason", mode="before")
    @classmethod
    def empty_reason(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if not isinstance(value, str):
            return value
        return _blank_to_none(value)


class ToolCribExceptionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    member_id: UUID
    tool_code: str
    reason: str | None
    status: ShopHoistRequestStatus
    created_by_kind: ActorKind
    created_by_id: str
    decided_by_kind: ActorKind | None = None
    decided_by_id: str | None = None


class ShopJobCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    notes: str | None = Field(default=None, max_length=2000)
    token_bounty: Decimal = Field(default=Decimal("0"), ge=0)

    @field_validator("title", mode="before")
    @classmethod
    def strip_title(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip()
        return value

    @field_validator("notes", mode="before")
    @classmethod
    def empty_notes(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if not isinstance(value, str):
            return value
        return _blank_to_none(value)


class ShopJobOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    notes: str | None
    token_bounty: Decimal
    status: ShopJobStatus
    claimed_by_member_id: UUID | None
    created_at: datetime
    updated_at: datetime


class FillDraftCreate(BaseModel):
    body: str = Field(min_length=1, max_length=4000)


class ChatDraftCreate(BaseModel):
    room_id: UUID
    body: str = Field(min_length=1, max_length=4000)


class StaffDraftOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    kind: DraftKind
    status: DraftStatus
    body: str
    room_id: UUID | None
    created_by_kind: ActorKind
    created_by_id: str
    accepted_by_kind: ActorKind | None = None
    accepted_by_id: str | None = None


class RefundRequestCreate(BaseModel):
    booking_id: UUID


class RefundRequestOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    booking_id: UUID
    status: ShopHoistRequestStatus
    created_by_kind: ActorKind
    created_by_id: str
    decided_by_kind: ActorKind | None = None
    decided_by_id: str | None = None


class StaffBalanceOut(BaseModel):
    member_id: UUID
    token_balance: Decimal
    actor_kind: ActorKind
    action_id: UUID


class OpenRequestsOut(BaseModel):
    shop_hoist: list[ShopHoistRequestOut]
    parts: list[StaffPartsRequestOut]
    tool_crib: list[ToolCribExceptionOut]
    actor_kind: ActorKind
    action_id: UUID


class StaffShopHoistRequestCreate(BaseModel):
    member_id: UUID
    hoist_id: UUID
    start_at: datetime
    end_at: datetime
    notes: str | None = Field(default=None, max_length=2000)


class JobEventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    member_id: UUID
    member_name: str | None = None
    job_key: str
    title: str
    kind: JobEventKind
    note: str | None
    claim_id: UUID | None
    created_at: datetime

    @classmethod
    def from_row(cls, row: JobEvent) -> JobEventOut:
        name = row.member.name if row.member is not None else None
        return cls.model_validate(row).model_copy(update={"member_name": name})


class JobClaimCreate(BaseModel):
    job_key: str = Field(min_length=1, max_length=80)
    note: str | None = Field(default=None, max_length=2000)

    @field_validator("job_key")
    @classmethod
    def strip_job_key(cls, value: str) -> str:
        return value.strip()

    @field_validator("note", mode="before")
    @classmethod
    def empty_note(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return _blank_to_none(str(value))


class JobDoneCreate(BaseModel):
    job_key: str = Field(min_length=1, max_length=80)
    note: str | None = Field(default=None, max_length=2000)

    @field_validator("job_key")
    @classmethod
    def strip_job_key(cls, value: str) -> str:
        return value.strip()

    @field_validator("note", mode="before")
    @classmethod
    def empty_note(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return _blank_to_none(str(value))
