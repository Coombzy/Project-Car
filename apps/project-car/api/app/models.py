"""Corrected Project Car shop domain (application spec §6).

Fixes applied from the retired ProjectCar-App/models.py notes:
- Python enums are enum.Enum; SQLAlchemy Enum is used only in mapped_column
- Member.tier_name column + Member.tier relationship (no doubled `tier`)
- IncidentSeverity is defined
- Incident.tool_id is a real FK; part_number stays denormalized display on Tool
- BillingTransaction.incident_id is a real FK
- Incident photos are JSON/JSONB lists of Nextcloud paths
- waitlist_entries is new
"""

from __future__ import annotations

import enum
import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import JSON, Uuid


class Base(DeclarativeBase):
    """Shop-OS metadata. Do not share with Nextcloud MariaDB."""


def _enum_column(enum_cls: type[enum.Enum], *, length: int = 32) -> SAEnum:
    return SAEnum(
        enum_cls,
        native_enum=False,
        length=length,
        values_callable=lambda items: [item.value for item in items],
    )


JsonList = JSON().with_variant(JSONB(), "postgresql")
JsonObject = JSON().with_variant(JSONB(), "postgresql")
UuidPk = Uuid(as_uuid=True).with_variant(UUID(as_uuid=True), "postgresql")


class MemberStatus(str, enum.Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    BANNED = "banned"
    CHURNED = "churned"


class HoistStatus(str, enum.Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    MAINTENANCE = "maintenance"
    LOCKED = "locked"


class BookingStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    ACTIVE = "active"
    COMPLETED = "completed"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class BookingKind(str, enum.Enum):
    CUSTOMER = "customer"
    SHOP = "shop"


class TokenTransactionKind(str, enum.Enum):
    BOOKING_RESERVE = "booking_reserve"
    BOOKING_DEBIT = "booking_debit"
    BOOKING_REFUND = "booking_refund"
    MONTHLY_ALLOCATION = "monthly_allocation"
    ADMIN_ADJUSTMENT = "admin_adjustment"


class IncidentSeverity(str, enum.Enum):
    MINOR = "minor"
    MODERATE = "moderate"
    SEVERE = "severe"
    CRITICAL = "critical"


class IncidentKind(str, enum.Enum):
    LATE_RETURN = "late_return"
    OTHER = "other"


class BillingKind(str, enum.Enum):
    MANUAL = "manual"
    DEPOSIT = "deposit"
    REFUND = "refund"


class AccessEventType(str, enum.Enum):
    CHECK_IN = "check_in"
    CHECK_OUT = "check_out"
    DENIED = "denied"


class NotificationChannel(str, enum.Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


class NotificationStatus(str, enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    DRY_RUN = "dry_run"
    SKIPPED = "skipped"


class FillOfferStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    CANCELLED = "cancelled"


class TodoStatus(str, enum.Enum):
    OPEN = "open"
    DONE = "done"


class PartsOrderStatus(str, enum.Enum):
    ORDERED = "ordered"
    SHIPPED = "shipped"
    IN_TRANSIT = "in_transit"
    RECEIVED = "received"


class CalendarProvider(str, enum.Enum):
    GOOGLE = "google"
    APPLE = "apple"


class MembershipTier(Base):
    """Membership plan. Prices and token allowances are data, not UI copy."""

    __tablename__ = "membership_tiers"

    name: Mapped[str] = mapped_column(String(64), primary_key=True)
    display_name: Mapped[str] = mapped_column(String(120), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=Decimal("0"))
    included_tokens: Mapped[int] = mapped_column(nullable=False, default=0)
    booking_window_days: Mapped[int] = mapped_column(nullable=False, default=14)
    max_simultaneous_bookings: Mapped[int] = mapped_column(nullable=False, default=1)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    members: Mapped[list[Member]] = relationship(back_populates="tier")

    def __repr__(self) -> str:
        return f"<MembershipTier(name={self.name!r})>"

    def __str__(self) -> str:
        return self.display_name


class Member(Base):
    """Paying customer. Staff/Member OIDC comes later; schema is ready now."""

    __tablename__ = "members"
    __table_args__ = (
        Index("ix_members_status", "status"),
        Index("ix_members_tier_name", "tier_name"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UuidPk, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True)
    phone: Mapped[Optional[str]] = mapped_column(String(40))
    tier_name: Mapped[str] = mapped_column(
        ForeignKey("membership_tiers.name", onupdate="CASCADE"),
        nullable=False,
    )
    status: Mapped[MemberStatus] = mapped_column(
        _enum_column(MemberStatus),
        nullable=False,
        default=MemberStatus.ACTIVE,
    )
    waiver_signed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    waiver_version: Mapped[Optional[str]] = mapped_column(String(64))
    emergency_contact_name: Mapped[Optional[str]] = mapped_column(String(200))
    emergency_contact_phone: Mapped[Optional[str]] = mapped_column(String(40))
    token_balance: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False, default=Decimal("0")
    )
    deposit_balance: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False, default=Decimal("0")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    tier: Mapped[MembershipTier] = relationship(back_populates="members")
    bookings: Mapped[list[Booking]] = relationship(
        back_populates="member", foreign_keys="Booking.member_id"
    )
    token_transactions: Mapped[list[TokenTransaction]] = relationship(back_populates="member")
    billing_transactions: Mapped[list[BillingTransaction]] = relationship(back_populates="member")
    access_events: Mapped[list[AccessEvent]] = relationship(back_populates="member")
    incidents_as_subject: Mapped[list[Incident]] = relationship(
        foreign_keys="Incident.member_id",
        back_populates="member",
    )
    incident_reports: Mapped[list[Incident]] = relationship(
        foreign_keys="Incident.reported_by_member_id",
        back_populates="reporter",
    )
    incidents_reviewed: Mapped[list[Incident]] = relationship(
        foreign_keys="Incident.reviewed_by_member_id",
        back_populates="reviewer",
    )
    notifications: Mapped[list[NotificationOutbox]] = relationship(back_populates="member")
    chat_participations: Mapped[list[ChatParticipant]] = relationship(back_populates="member")
    todos: Mapped[list[Todo]] = relationship(back_populates="member")

    def __repr__(self) -> str:
        return f"<Member(id={self.id!r}, email={self.email!r})>"

    def __str__(self) -> str:
        return self.name


class Hoist(Base):
    """Work bay / 2-post hoist. Exactly one row should be the shop hoist."""

    __tablename__ = "hoists"
    __table_args__ = (Index("ix_hoists_status", "status"),)

    id: Mapped[uuid.UUID] = mapped_column(UuidPk, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    location_label: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    status: Mapped[HoistStatus] = mapped_column(
        _enum_column(HoistStatus),
        nullable=False,
        default=HoistStatus.AVAILABLE,
    )
    is_shop: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    bookings: Mapped[list[Booking]] = relationship(back_populates="hoist")
    incidents: Mapped[list[Incident]] = relationship(back_populates="hoist")

    def __repr__(self) -> str:
        return f"<Hoist(id={self.id!r}, name={self.name!r})>"

    def __str__(self) -> str:
        return self.name


class Tool(Base):
    """Shared tool inventory. Schema now; checkout UI later."""

    __tablename__ = "tools"

    id: Mapped[uuid.UUID] = mapped_column(UuidPk, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    part_number: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    incidents: Mapped[list[Incident]] = relationship(back_populates="tool")

    def __repr__(self) -> str:
        return f"<Tool(id={self.id!r}, part_number={self.part_number!r})>"

    def __str__(self) -> str:
        return f"{self.name} ({self.part_number})"


class Booking(Base):
    """Hoist reservation. Customer rows reserve tokens; shop rows are Owner-only."""

    __tablename__ = "bookings"
    __table_args__ = (
        Index("ix_bookings_hoist_status", "hoist_id", "status"),
        Index("ix_bookings_member_status", "member_id", "status"),
        Index("ix_bookings_start_at", "start_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UuidPk, primary_key=True, default=uuid.uuid4)
    member_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("members.id", ondelete="RESTRICT"), nullable=True
    )
    hoist_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("hoists.id", ondelete="RESTRICT"), nullable=False
    )
    start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    kind: Mapped[BookingKind] = mapped_column(
        _enum_column(BookingKind),
        nullable=False,
        default=BookingKind.CUSTOMER,
    )
    status: Mapped[BookingStatus] = mapped_column(
        _enum_column(BookingStatus),
        nullable=False,
        default=BookingStatus.PENDING,
    )
    reserved_tokens: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False, default=Decimal("0")
    )
    pricing_rule: Mapped[Optional[dict]] = mapped_column(JsonObject)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    member: Mapped[Optional[Member]] = relationship(back_populates="bookings", foreign_keys=[member_id])
    hoist: Mapped[Hoist] = relationship(back_populates="bookings")
    token_transactions: Mapped[list[TokenTransaction]] = relationship(back_populates="booking")
    incidents: Mapped[list[Incident]] = relationship(back_populates="booking")

    def __repr__(self) -> str:
        return f"<Booking(id={self.id!r}, status={self.status!r})>"

    def __str__(self) -> str:
        return f"Booking {self.id} ({self.status.value})"


class TokenTransaction(Base):
    """Append-only token ledger. member.token_balance is a cached sum."""

    __tablename__ = "token_transactions"
    __table_args__ = (Index("ix_token_transactions_member_created", "member_id", "created_at"),)

    id: Mapped[uuid.UUID] = mapped_column(UuidPk, primary_key=True, default=uuid.uuid4)
    member_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("members.id", ondelete="RESTRICT"), nullable=False
    )
    booking_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("bookings.id", ondelete="SET NULL")
    )
    kind: Mapped[TokenTransactionKind] = mapped_column(
        _enum_column(TokenTransactionKind, length=40),
        nullable=False,
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    note: Mapped[Optional[str]] = mapped_column(Text)
    meta: Mapped[Optional[dict]] = mapped_column(JsonObject)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    member: Mapped[Member] = relationship(back_populates="token_transactions")
    booking: Mapped[Optional[Booking]] = relationship(back_populates="token_transactions")

    def __repr__(self) -> str:
        return f"<TokenTransaction(id={self.id!r}, kind={self.kind!r}, amount={self.amount!r})>"

    def __str__(self) -> str:
        return f"{self.kind.value} {self.amount}"


class WaitlistEntry(Base):
    """Public waitlist row: name, email, optional phone/notes, timestamp."""

    __tablename__ = "waitlist_entries"
    __table_args__ = (
        UniqueConstraint("email", name="uq_waitlist_entries_email"),
        Index("ix_waitlist_entries_created_at", "created_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UuidPk, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(40))
    notes: Mapped[Optional[str]] = mapped_column(Text)
    contacted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"<WaitlistEntry(id={self.id!r}, email={self.email!r})>"

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"


class Incident(Base):
    """Owner-filed incident. Multi-FK to Member is split by role."""

    __tablename__ = "incidents"
    __table_args__ = (
        Index("ix_incidents_member_id", "member_id"),
        Index("ix_incidents_severity", "severity"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UuidPk, primary_key=True, default=uuid.uuid4)
    member_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("members.id", ondelete="SET NULL")
    )
    reported_by_member_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("members.id", ondelete="SET NULL")
    )
    reviewed_by_member_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("members.id", ondelete="SET NULL")
    )
    hoist_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("hoists.id", ondelete="SET NULL")
    )
    booking_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("bookings.id", ondelete="SET NULL")
    )
    tool_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("tools.id", ondelete="SET NULL")
    )
    kind: Mapped[IncidentKind] = mapped_column(
        _enum_column(IncidentKind),
        nullable=False,
        default=IncidentKind.OTHER,
    )
    severity: Mapped[IncidentSeverity] = mapped_column(
        _enum_column(IncidentSeverity),
        nullable=False,
        default=IncidentSeverity.MINOR,
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    photos: Mapped[list[str]] = mapped_column(JsonList, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    member: Mapped[Optional[Member]] = relationship(
        foreign_keys=[member_id],
        back_populates="incidents_as_subject",
    )
    reporter: Mapped[Optional[Member]] = relationship(
        foreign_keys=[reported_by_member_id],
        back_populates="incident_reports",
    )
    reviewer: Mapped[Optional[Member]] = relationship(
        foreign_keys=[reviewed_by_member_id],
        back_populates="incidents_reviewed",
    )
    hoist: Mapped[Optional[Hoist]] = relationship(back_populates="incidents")
    booking: Mapped[Optional[Booking]] = relationship(back_populates="incidents")
    tool: Mapped[Optional[Tool]] = relationship(back_populates="incidents")
    billing_transactions: Mapped[list[BillingTransaction]] = relationship(
        back_populates="incident"
    )

    def __repr__(self) -> str:
        return f"<Incident(id={self.id!r}, severity={self.severity!r})>"

    def __str__(self) -> str:
        return f"{self.kind.value} ({self.severity.value})"


class BillingTransaction(Base):
    """Manual billing record only. No payment processor in v1."""

    __tablename__ = "billing_transactions"
    __table_args__ = (Index("ix_billing_transactions_member_created", "member_id", "created_at"),)

    id: Mapped[uuid.UUID] = mapped_column(UuidPk, primary_key=True, default=uuid.uuid4)
    member_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("members.id", ondelete="RESTRICT"), nullable=False
    )
    incident_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("incidents.id", ondelete="SET NULL")
    )
    kind: Mapped[BillingKind] = mapped_column(
        _enum_column(BillingKind),
        nullable=False,
        default=BillingKind.MANUAL,
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    note: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    member: Mapped[Member] = relationship(back_populates="billing_transactions")
    incident: Mapped[Optional[Incident]] = relationship(back_populates="billing_transactions")

    def __repr__(self) -> str:
        return f"<BillingTransaction(id={self.id!r}, amount={self.amount!r})>"

    def __str__(self) -> str:
        return f"{self.kind.value} {self.amount}"


class AccessEvent(Base):
    """Access log schema. No NFC/FOB readers in this slice."""

    __tablename__ = "access_events"
    __table_args__ = (
        Index("ix_access_events_member_occurred", "member_id", "occurred_at"),
        Index("ix_access_events_reader_occurred", "reader_location", "occurred_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UuidPk, primary_key=True, default=uuid.uuid4)
    member_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("members.id", ondelete="SET NULL")
    )
    reader_location: Mapped[str] = mapped_column(String(120), nullable=False, default="")
    event_type: Mapped[AccessEventType] = mapped_column(
        _enum_column(AccessEventType),
        nullable=False,
    )
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    payload: Mapped[Optional[dict]] = mapped_column(JSON)

    member: Mapped[Optional[Member]] = relationship(back_populates="access_events")

    def __repr__(self) -> str:
        return f"<AccessEvent(id={self.id!r}, event_type={self.event_type!r})>"

    def __str__(self) -> str:
        return f"{self.event_type.value} @ {self.reader_location}"


class FillOffer(Base):
    """Owner-published next-day fill discount. One row per Regina calendar day."""

    __tablename__ = "fill_offers"
    __table_args__ = (UniqueConstraint("target_date", name="uq_fill_offers_target_date"),)

    id: Mapped[uuid.UUID] = mapped_column(UuidPk, primary_key=True, default=uuid.uuid4)
    target_date: Mapped[date] = mapped_column(Date, nullable=False)
    window_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    window_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    open_hours: Mapped[Decimal] = mapped_column(Numeric(12, 4), nullable=False, default=Decimal("0"))
    booked_hours: Mapped[Decimal] = mapped_column(Numeric(12, 4), nullable=False, default=Decimal("0"))
    capacity_hours: Mapped[Decimal] = mapped_column(Numeric(12, 4), nullable=False, default=Decimal("0"))
    discount_pct: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False, default=Decimal("0"))
    fill_multiplier: Mapped[Decimal] = mapped_column(Numeric(8, 4), nullable=False, default=Decimal("1"))
    urgency: Mapped[str] = mapped_column(String(16), nullable=False, default="none")
    status: Mapped[FillOfferStatus] = mapped_column(
        _enum_column(FillOfferStatus),
        nullable=False,
        default=FillOfferStatus.DRAFT,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    notifications: Mapped[list[NotificationOutbox]] = relationship(back_populates="fill_offer")

    def __repr__(self) -> str:
        return f"<FillOffer(target_date={self.target_date!r}, discount_pct={self.discount_pct!r})>"


class NotificationOutbox(Base):
    """Durable notification queue. Adapters mark sent / skipped / failed."""

    __tablename__ = "notification_outbox"
    __table_args__ = (
        Index("ix_notification_outbox_status_created", "status", "created_at"),
        Index("ix_notification_outbox_member_created", "member_id", "created_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UuidPk, primary_key=True, default=uuid.uuid4)
    channel: Mapped[NotificationChannel] = mapped_column(
        _enum_column(NotificationChannel),
        nullable=False,
    )
    member_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("members.id", ondelete="SET NULL")
    )
    fill_offer_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("fill_offers.id", ondelete="SET NULL")
    )
    to_address: Mapped[Optional[str]] = mapped_column(String(320))
    subject: Mapped[Optional[str]] = mapped_column(String(240))
    body: Mapped[Optional[str]] = mapped_column(Text)
    payload: Mapped[Optional[dict]] = mapped_column(JsonObject)
    status: Mapped[NotificationStatus] = mapped_column(
        _enum_column(NotificationStatus),
        nullable=False,
        default=NotificationStatus.PENDING,
    )
    attempts: Mapped[int] = mapped_column(nullable=False, default=0)
    last_error: Mapped[Optional[str]] = mapped_column(String(500))
    dry_run: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    member: Mapped[Optional[Member]] = relationship(back_populates="notifications")
    fill_offer: Mapped[Optional[FillOffer]] = relationship(back_populates="notifications")

    def __repr__(self) -> str:
        return f"<NotificationOutbox(id={self.id!r}, channel={self.channel!r}, status={self.status!r})>"


class ChatSenderRole(str, enum.Enum):
    OWNER = "owner"
    MEMBER = "member"


class ChatRoom(Base):
    """Human shop thread. Owners start rooms; members reply if they are in them."""

    __tablename__ = "chat_rooms"
    __table_args__ = (Index("ix_chat_rooms_updated_at", "updated_at"),)

    id: Mapped[uuid.UUID] = mapped_column(UuidPk, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    created_by_email: Mapped[str] = mapped_column(String(320), nullable=False)
    muted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    participants: Mapped[list[ChatParticipant]] = relationship(
        back_populates="room", cascade="all, delete-orphan"
    )
    messages: Mapped[list[ChatMessage]] = relationship(
        back_populates="room", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<ChatRoom(id={self.id!r}, title={self.title!r})>"

    def __str__(self) -> str:
        return self.title


class ChatParticipant(Base):
    """Member in a room. Owner/ops are implicit (see-all), not rows here."""

    __tablename__ = "chat_participants"
    __table_args__ = (
        UniqueConstraint("room_id", "member_id", name="uq_chat_participants_room_member"),
        Index("ix_chat_participants_member_id", "member_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UuidPk, primary_key=True, default=uuid.uuid4)
    room_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("chat_rooms.id", ondelete="CASCADE"), nullable=False
    )
    member_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("members.id", ondelete="CASCADE"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    room: Mapped[ChatRoom] = relationship(back_populates="participants")
    member: Mapped[Member] = relationship(back_populates="chat_participations")

    def __repr__(self) -> str:
        return f"<ChatParticipant(room_id={self.room_id!r}, member_id={self.member_id!r})>"


class ChatMessage(Base):
    """One human message. No AI/Grok/Matrix sender in Chat v1."""

    __tablename__ = "chat_messages"
    __table_args__ = (
        Index("ix_chat_messages_room_created", "room_id", "created_at"),
        Index("ix_chat_messages_room_seq", "room_id", "seq", unique=True),
    )

    id: Mapped[uuid.UUID] = mapped_column(UuidPk, primary_key=True, default=uuid.uuid4)
    room_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("chat_rooms.id", ondelete="CASCADE"), nullable=False
    )
    sender_role: Mapped[ChatSenderRole] = mapped_column(
        _enum_column(ChatSenderRole),
        nullable=False,
    )
    sender_member_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("members.id", ondelete="SET NULL")
    )
    sender_email: Mapped[str] = mapped_column(String(320), nullable=False)
    sender_name: Mapped[str] = mapped_column(String(200), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    seq: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    room: Mapped[ChatRoom] = relationship(back_populates="messages")
    sender_member: Mapped[Optional[Member]] = relationship()

    def __repr__(self) -> str:
        return f"<ChatMessage(id={self.id!r}, room_id={self.room_id!r})>"


class Todo(Base):
    """Personal to-do for the logged-in Owner or Member. Not Nextcloud Deck."""

    __tablename__ = "todos"
    __table_args__ = (
        Index("ix_todos_owner_email_status", "owner_email", "status"),
        Index("ix_todos_member_status", "member_id", "status"),
        Index("ix_todos_due_at", "due_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UuidPk, primary_key=True, default=uuid.uuid4)
    owner_email: Mapped[Optional[str]] = mapped_column(String(320))
    member_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("members.id", ondelete="CASCADE")
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    due_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    status: Mapped[TodoStatus] = mapped_column(
        _enum_column(TodoStatus),
        nullable=False,
        default=TodoStatus.OPEN,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    member: Mapped[Optional[Member]] = relationship(back_populates="todos")

    def __repr__(self) -> str:
        return f"<Todo(id={self.id!r}, title={self.title!r})>"


class PartsOrder(Base):
    """Ops parts PO stub. SKUs use the PT prefix; not a live vendor API."""

    __tablename__ = "parts_orders"
    __table_args__ = (
        UniqueConstraint("po_number", name="uq_parts_orders_po_number"),
        Index("ix_parts_orders_status_ordered", "status", "ordered_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UuidPk, primary_key=True, default=uuid.uuid4)
    po_number: Mapped[str] = mapped_column(String(40), nullable=False)
    sku: Mapped[Optional[str]] = mapped_column(String(80))
    what: Mapped[str] = mapped_column(String(240), nullable=False)
    vendor: Mapped[str] = mapped_column(String(160), nullable=False, default="")
    for_label: Mapped[str] = mapped_column(String(160), nullable=False, default="")
    status: Mapped[PartsOrderStatus] = mapped_column(
        _enum_column(PartsOrderStatus),
        nullable=False,
        default=PartsOrderStatus.ORDERED,
    )
    ordered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    shipped_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    eta_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    received_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    tracking: Mapped[Optional[str]] = mapped_column(String(120))
    notes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<PartsOrder(po_number={self.po_number!r}, status={self.status!r})>"


class CalendarConnection(Base):
    """Scaffold for Google / Apple calendar OAuth. Not production-complete."""

    __tablename__ = "calendar_connections"
    __table_args__ = (
        UniqueConstraint("owner_email", "member_id", "provider", name="uq_calendar_connections_owner_provider"),
        Index("ix_calendar_connections_member", "member_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UuidPk, primary_key=True, default=uuid.uuid4)
    owner_email: Mapped[Optional[str]] = mapped_column(String(320))
    member_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("members.id", ondelete="CASCADE")
    )
    provider: Mapped[CalendarProvider] = mapped_column(
        _enum_column(CalendarProvider),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="disconnected")
    external_account: Mapped[Optional[str]] = mapped_column(String(320))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<CalendarConnection(provider={self.provider!r}, status={self.status!r})>"


ALL_MODELS = [
    MembershipTier,
    Member,
    Hoist,
    Tool,
    Booking,
    TokenTransaction,
    WaitlistEntry,
    Incident,
    BillingTransaction,
    AccessEvent,
    FillOffer,
    NotificationOutbox,
    ChatRoom,
    ChatParticipant,
    ChatMessage,
    Todo,
    PartsOrder,
    CalendarConnection,
]


if __name__ == "__main__":
    for model in ALL_MODELS:
        table = model.__table__
        print(f"{table.name}: {len(table.columns)} columns")
