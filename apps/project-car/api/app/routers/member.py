"""Member self-serve: own balance, quote, book / confirm / cancel.

Reuses Owner booking services (duration × band × overlay + ledger). Members
act only on their own rows. Bays 1-5 are a direct booking. The shop hoist is
a pending request until a person or an AI approves it.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.deps import DbSession, MemberUser
from app.models import (
    ActorKind,
    Booking,
    BookingKind,
    BookingStatus,
    Hoist,
    Member,
    TokenTransaction,
)
from app.schemas import (
    BookingOut,
    BookingQuoteOut,
    FillPreviewOut,
    HoistOut,
    MemberBookingCreate,
    MemberBookingQuoteRequest,
    MemberDashboardOut,
    MemberRateChartOut,
    MemberScheduleOut,
    MemberSelfOut,
    OccupancyOut,
    PricingRuleOut,
    ShopHoistRequestOut,
    ShopJobOut,
    ToolCribExceptionCreate,
    ToolCribExceptionOut,
    MemberTokenPurchaseCreate,
    TokenTransactionOut,
)
from app.routers.dashboard import member_dashboard_payload
from app.routers.members import MAX_TOKEN_ADJUSTMENT
from app.services import bookings as booking_service
from app.services.fill import snapshot_next_day
from app.services.payments import get_payment_processor
from app.services.peak_cap import PEAK_BAND_IDS, PEAK_HOURS_PER_WEEK
from app.services.pricing import weekly_rate_chart
from app.services.shop_hoist_requests import (
    create_shop_hoist_request,
    get_shop_hoist,
    list_shop_hoist_requests,
)
from app.services.staff import claim_job, create_tool_crib_exception
from app.services.tokens import record_token_purchase
from app.shop_time import as_utc

router = APIRouter(prefix="/member", tags=["member"])


def _forbidden(message: str = "Members can only act on their own bookings.") -> HTTPException:
    return HTTPException(status_code=403, detail={"code": "forbidden", "message": message})


def _own_member(session, principal: MemberUser) -> Member:
    member = session.scalars(
        select(Member).options(selectinload(Member.tier)).where(Member.id == principal.member_id)
    ).first()
    if member is None:
        raise HTTPException(
            status_code=401,
            detail={"code": "unauthorized", "message": "Member authentication required."},
        )
    return member


def _own_booking(session, principal: MemberUser, booking_id: UUID) -> Booking:
    booking = booking_service.get_booking(session, booking_id)
    if booking.member_id != principal.member_id:
        raise _forbidden()
    return booking


def _customer_hoists(session) -> list[Hoist]:
    return list(
        session.scalars(select(Hoist).where(Hoist.is_shop.is_(False)).order_by(Hoist.name)).all()
    )


def _ics_escape(value: str) -> str:
    normalized = value.replace("\r\n", "\n").replace("\r", "\n")
    return (
        normalized.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )


def _ics_utc(value: datetime) -> str:
    # SQLite returns the stored UTC instant with no offset. as_utc() would
    # read that bare clock as shop wall time and shift the calendar file.
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    else:
        value = value.astimezone(timezone.utc)
    return value.strftime("%Y%m%dT%H%M%SZ")


def _ics_utf8_prefix(text: str, max_octets: int) -> str:
    """Longest prefix whose UTF-8 encoding is at most max_octets."""
    encoded = text.encode("utf-8")
    if max_octets <= 0 or not encoded:
        return ""
    if len(encoded) <= max_octets:
        return text
    cut = max_octets
    # Walk off a trailing continuation byte so the cut is not mid-character.
    while cut > 0 and (encoded[cut] & 0xC0) == 0x80:
        cut -= 1
    return encoded[:cut].decode("utf-8")


def _fold_ics_line(content: str) -> str:
    """Fold one content line to at most 75 UTF-8 octets (RFC 5545 §3.1).

    A continuation starts with one space, and that space counts toward 75.
    The cut is never inside a multibyte character. ASCII folds the same way:
    the to-do exporter's character fold can leave an 81-octet first line.
    """
    if len(content.encode("utf-8")) <= 75:
        return content
    parts: list[str] = []
    rest = content
    limit = 75
    while rest:
        piece = _ics_utf8_prefix(rest, limit)
        if not piece:
            piece = rest[0]
        parts.append(piece)
        rest = rest[len(piece):]
        limit = 74
    return "\r\n ".join(parts)


def _booking_ics(booking: Booking) -> str:
    """One VEVENT. Start and end are UTC. The shop label is Mountain Time."""
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Project Car//Shop OS//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-TIMEZONE:Mountain Time",
        "BEGIN:VEVENT",
        f"UID:{booking.id}",
        f"DTSTAMP:{_ics_utc(datetime.now(timezone.utc))}",
        f"DTSTART:{_ics_utc(booking.start_at)}",
        f"DTEND:{_ics_utc(booking.end_at)}",
        f"SUMMARY:{_ics_escape(booking.hoist.name)}",
        "COMMENT:Times are UTC. Shop local time is Mountain Time.",
        "END:VEVENT",
        "END:VCALENDAR",
    ]
    return "\r\n".join(_fold_ics_line(line) for line in lines) + "\r\n"


@router.get("/rates", response_model=MemberRateChartOut)
def member_rates(session: DbSession, _principal: MemberUser) -> MemberRateChartOut:
    chart = weekly_rate_chart(
        session,
        peak_band_ids=PEAK_BAND_IDS,
        peak_cap_hours=PEAK_HOURS_PER_WEEK,
    )
    return MemberRateChartOut.model_validate(chart)


@router.get("/me", response_model=MemberSelfOut)
def member_me(session: DbSession, principal: MemberUser) -> MemberSelfOut:
    booking_service.settle_elapsed_no_shows(session)
    member = session.scalars(
        select(Member)
        .options(
            selectinload(Member.tier),
            selectinload(Member.bookings).selectinload(Booking.hoist),
            selectinload(Member.bookings).selectinload(Booking.member),
            selectinload(Member.token_transactions),
        )
        .where(Member.id == principal.member_id)
    ).first()
    if member is None:
        raise HTTPException(
            status_code=401,
            detail={"code": "unauthorized", "message": "Member authentication required."},
        )
    bookings = sorted(member.bookings, key=lambda row: row.start_at, reverse=True)
    tokens = sorted(member.token_transactions, key=lambda row: row.created_at, reverse=True)
    return MemberSelfOut(
        id=member.id,
        name=member.name,
        email=member.email,
        phone=member.phone,
        tier_name=member.tier_name,
        status=member.status,
        waiver_signed_at=member.waiver_signed_at,
        waiver_version=member.waiver_version,
        emergency_contact_name=member.emergency_contact_name,
        emergency_contact_phone=member.emergency_contact_phone,
        token_balance=member.token_balance,
        allowance_balance=member.allowance_balance,
        purchased_balance=member.purchased_balance,
        deposit_balance=member.deposit_balance,
        created_at=member.created_at,
        updated_at=member.updated_at,
        booking_window_days=member.tier.booking_window_days,
        max_simultaneous_bookings=member.tier.max_simultaneous_bookings,
        included_tokens=member.tier.included_tokens,
        bookings=[BookingOut.from_booking(row) for row in bookings],
        tokens=[TokenTransactionOut.model_validate(row) for row in tokens],
    )


@router.get("/dashboard", response_model=MemberDashboardOut)
def member_dashboard(session: DbSession, principal: MemberUser) -> MemberDashboardOut:
    booking_service.settle_elapsed_no_shows(session)
    return member_dashboard_payload(session, principal)


@router.get("/tokens", response_model=list[TokenTransactionOut])
def member_tokens(
    session: DbSession,
    principal: MemberUser,
    limit: int = Query(default=200, ge=1, le=500),
) -> list[TokenTransactionOut]:
    rows = session.scalars(
        select(TokenTransaction)
        .where(TokenTransaction.member_id == principal.member_id)
        .order_by(TokenTransaction.created_at.desc())
        .limit(limit)
    ).all()
    return [TokenTransactionOut.model_validate(row) for row in rows]


@router.get("/hoists", response_model=list[HoistOut])
def member_hoists(session: DbSession, _principal: MemberUser) -> list[HoistOut]:
    return [HoistOut.model_validate(row) for row in _customer_hoists(session)]


@router.get("/bookings", response_model=list[BookingOut])
def member_bookings(
    session: DbSession,
    principal: MemberUser,
    hoist_id: UUID | None = None,
    window_start: datetime | None = Query(default=None),
    window_end: datetime | None = Query(default=None),
    limit: int = Query(default=200, ge=1, le=500),
) -> list[BookingOut]:
    booking_service.settle_elapsed_no_shows(session)
    stmt = (
        select(Booking)
        .options(selectinload(Booking.member), selectinload(Booking.hoist))
        .where(Booking.member_id == principal.member_id)
    )
    if hoist_id is not None:
        stmt = stmt.where(Booking.hoist_id == hoist_id)
    if window_start is not None:
        stmt = stmt.where(Booking.end_at > as_utc(window_start))
    if window_end is not None:
        stmt = stmt.where(Booking.start_at < as_utc(window_end))
    # Latest `limit` by start, then oldest-first so a short list matches today's order.
    latest = list(session.scalars(stmt.order_by(Booking.start_at.desc()).limit(limit)).all())
    latest.reverse()
    return [BookingOut.from_booking(row) for row in latest]


@router.get("/schedule", response_model=MemberScheduleOut)
def member_schedule(
    session: DbSession,
    principal: MemberUser,
    window_start: datetime | None = Query(default=None),
    window_end: datetime | None = Query(default=None),
) -> MemberScheduleOut:
    booking_service.settle_elapsed_no_shows(session)
    hoists = _customer_hoists(session)
    hoist_ids = [row.id for row in hoists]
    stmt = (
        select(Booking)
        .options(selectinload(Booking.member), selectinload(Booking.hoist))
        .where(
            Booking.hoist_id.in_(hoist_ids),
            Booking.kind == BookingKind.CUSTOMER,
            Booking.status.in_(booking_service.OPEN_STATUSES),
        )
        .order_by(Booking.start_at)
    )
    if window_start is not None:
        stmt = stmt.where(Booking.end_at > as_utc(window_start))
    if window_end is not None:
        stmt = stmt.where(Booking.start_at < as_utc(window_end))
    rows = session.scalars(stmt).all()
    own: list[BookingOut] = []
    occupancy: list[OccupancyOut] = []
    for row in rows:
        occupancy.append(
            OccupancyOut(
                booking_id=row.id,
                hoist_id=row.hoist_id,
                hoist_name=row.hoist.name,
                start_at=row.start_at,
                end_at=row.end_at,
                status=row.status,
                own=row.member_id == principal.member_id,
            )
        )
        if row.member_id == principal.member_id:
            own.append(BookingOut.from_booking(row))
    return MemberScheduleOut(
        hoists=[HoistOut.model_validate(row) for row in hoists],
        bookings=own,
        occupancy=occupancy,
    )


@router.get("/fill", response_model=FillPreviewOut)
def member_fill(session: DbSession, _principal: MemberUser) -> FillPreviewOut:
    return FillPreviewOut.from_snapshot(snapshot_next_day(session))


@router.post("/bookings/quote", response_model=BookingQuoteOut)
def member_quote(
    body: MemberBookingQuoteRequest,
    session: DbSession,
    principal: MemberUser,
) -> BookingQuoteOut:
    quote, balance, after = booking_service.preview_reserve(
        session,
        start_at=body.start_at,
        end_at=body.end_at,
        member_id=principal.member_id,
    )
    return BookingQuoteOut(
        pricing_rule=PricingRuleOut.model_validate(quote.as_rule()),
        reserved_tokens=quote.final_reserve_cost,
        token_balance=balance,
        token_balance_after=after,
    )


@router.get("/shop-hoist", response_model=HoistOut)
def member_shop_hoist(session: DbSession, _principal: MemberUser) -> HoistOut:
    return HoistOut.model_validate(get_shop_hoist(session))


@router.get("/shop-hoist-requests", response_model=list[ShopHoistRequestOut])
def member_shop_hoist_requests(
    session: DbSession, principal: MemberUser
) -> list[ShopHoistRequestOut]:
    rows = list_shop_hoist_requests(session, member_id=principal.member_id)
    return [ShopHoistRequestOut.from_row(row) for row in rows]


@router.post("/shop-hoist-requests", response_model=ShopHoistRequestOut, status_code=201)
def member_create_shop_hoist_request(
    body: MemberBookingCreate,
    session: DbSession,
    principal: MemberUser,
) -> ShopHoistRequestOut:
    if body.hoist_id is None:
        raise HTTPException(
            status_code=400,
            detail={"code": "hoist_required", "message": "A shop hoist request needs a bay."},
        )
    row = create_shop_hoist_request(
        session,
        member_id=principal.member_id,
        hoist_id=body.hoist_id,
        start_at=body.start_at,
        end_at=body.end_at,
        notes=body.notes,
        created_by_kind=ActorKind.HUMAN,
        created_by_id=str(principal.member_id),
    )
    return ShopHoistRequestOut.from_row(row)


@router.post("/bookings", status_code=201)
def member_create_booking(
    body: MemberBookingCreate,
    session: DbSession,
    principal: MemberUser,
) -> BookingOut | ShopHoistRequestOut:
    _own_member(session, principal)
    hoist = session.get(Hoist, body.hoist_id) if body.hoist_id is not None else None
    if hoist is not None and hoist.is_shop:
        row = create_shop_hoist_request(
            session,
            member_id=principal.member_id,
            hoist_id=body.hoist_id,
            start_at=body.start_at,
            end_at=body.end_at,
            notes=body.notes,
            created_by_kind=ActorKind.HUMAN,
            created_by_id=str(principal.member_id),
        )
        return ShopHoistRequestOut.from_row(row)
    booking = booking_service.create_booking(
        session,
        member_id=principal.member_id,
        hoist_id=body.hoist_id,
        start_at=body.start_at,
        end_at=body.end_at,
        notes=body.notes,
        kind=BookingKind.CUSTOMER,
        shown_tokens=body.tokens,
        confirm=True,
    )
    return BookingOut.from_booking(booking)


@router.post("/bookings/{booking_id}/confirm", response_model=BookingOut)
def member_confirm_booking(
    booking_id: UUID,
    session: DbSession,
    principal: MemberUser,
) -> BookingOut:
    _own_booking(session, principal, booking_id)
    return BookingOut.from_booking(booking_service.confirm_booking(session, booking_id))


@router.post("/bookings/{booking_id}/cancel", response_model=BookingOut)
def member_cancel_booking(
    booking_id: UUID,
    session: DbSession,
    principal: MemberUser,
) -> BookingOut:
    _own_booking(session, principal, booking_id)
    return BookingOut.from_booking(booking_service.cancel_booking(session, booking_id, by_member=True))


@router.get("/bookings/{booking_id}/ics")
def member_booking_ics(
    booking_id: UUID, session: DbSession, principal: MemberUser
) -> Response:
    booking = booking_service.get_booking(session, booking_id)
    # 404, not the 403 used by confirm/cancel, so the URL does not confirm
    # that another member's booking id exists.
    if booking.member_id != principal.member_id:
        raise HTTPException(
            status_code=404,
            detail={"code": "not_found", "message": "Booking not found."},
        )
    if booking.status == BookingStatus.CANCELLED:
        raise HTTPException(
            status_code=409,
            detail={
                "code": "booking_cancelled",
                "message": "A cancelled booking cannot be added to a calendar.",
            },
        )
    payload = _booking_ics(booking)
    return Response(
        content=payload,
        media_type="text/calendar; charset=utf-8",
        headers={
            "Content-Disposition": (
                f'attachment; filename="project-car-booking-{booking.id}.ics"'
            ),
            "Cache-Control": "no-store",
        },
    )


@router.post("/tool-crib-exceptions", response_model=ToolCribExceptionOut, status_code=201)
def member_create_tool_crib_exception(
    body: ToolCribExceptionCreate,
    session: DbSession,
    principal: MemberUser,
) -> ToolCribExceptionOut:
    row = create_tool_crib_exception(
        session,
        member_id=principal.member_id,
        tool_code=body.tool_code,
        reason=body.reason,
        created_by_kind=ActorKind.HUMAN,
        created_by_id=str(principal.member_id),
    )
    return ToolCribExceptionOut.model_validate(row)


@router.post("/jobs/{job_id}/claim", response_model=ShopJobOut)
def member_claim_job(job_id: UUID, session: DbSession, principal: MemberUser) -> ShopJobOut:
    return ShopJobOut.model_validate(claim_job(session, job_id, principal.member_id))


@router.post("/token-purchases", response_model=TokenTransactionOut, status_code=201)
def member_buy_tokens(
    body: MemberTokenPurchaseCreate,
    session: DbSession,
    principal: MemberUser,
) -> TokenTransactionOut:
    """Collect through the payment adapter, then credit the purchased pile."""
    if body.tokens >= MAX_TOKEN_ADJUSTMENT:
        raise HTTPException(
            status_code=400,
            detail={"code": "invalid_tokens", "message": "A purchase must be under 1,000,000 tokens."},
        )
    processor = get_payment_processor()
    receipt = processor.collect(
        member_id=principal.member_id,
        tokens=body.tokens,
        subtotal_cad=body.subtotal_cad,
        payment_id=body.payment_id,
    )
    member = booking_service.lock_member(session, principal.member_id)
    row = record_token_purchase(
        session,
        member,
        payment_id=receipt.payment_id,
        tokens=body.tokens,
        subtotal_cad=receipt.subtotal_cad,
        recorded_by=member.email,
        processor=receipt.processor,
    )
    session.refresh(row)
    return TokenTransactionOut.model_validate(row)
