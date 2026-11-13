import { memberCancelBookingAction, memberConfirmBookingAction } from "../app/member/schedule/actions";
import { memberCancelOffer } from "../lib/booking-calendar";
import { bookingStatusLabel } from "../lib/booking-words";
import { formatCalendarTime } from "../lib/calendar";
import type { Booking, Occupancy } from "../lib/config";
import { shopClock } from "../lib/time";
import { BookingCost } from "./booking-cost";
import { ScheduleReturnFields, type ScheduleReturn } from "./schedule-return-fields";

export function MemberBookingCard({
  slot,
  own,
  returnTo,
  compact,
}: {
  slot: Occupancy;
  own?: Booking;
  returnTo: ScheduleReturn;
  compact?: boolean;
}) {
  const cancel = own
    ? memberCancelOffer(
        { status: own.status, startAt: own.start_at, reservedTokens: own.reserved_tokens },
        shopClock(),
      )
    : null;
  return (
    <article
      className={`booking-chip status-${slot.status}${slot.own ? "" : " occupancy-chip"}${compact ? " booking-chip-hour" : ""}`}
    >
      <strong>{slot.own ? "You" : "Booked"}</strong>
      <div>
        {compact ? null : <>{slot.hoist_name} · </>}
        {formatCalendarTime(slot.start_at)}–{formatCalendarTime(slot.end_at)}
      </div>
      {own ? <BookingCost reservedTokens={own.reserved_tokens} pricingRule={own.pricing_rule} /> : null}
      <span className={`pill pill-${slot.status}`}>{bookingStatusLabel(slot.status)}</span>
      {own && own.status === "pending" ? (
        <div className="chip-actions">
          <form action={memberConfirmBookingAction}>
            <ScheduleReturnFields returnTo={returnTo} />
            <input type="hidden" name="id" value={own.id} />
            <button type="submit">Confirm</button>
          </form>
          {own.status === "pending" && cancel !== null && cancel.visible ? (
            <form action={memberCancelBookingAction}>
              <ScheduleReturnFields returnTo={returnTo} />
              <input type="hidden" name="id" value={own.id} />
              <button className="ghost" type="submit">
                {cancel.label}
              </button>
            </form>
          ) : null}
        </div>
      ) : null}
      {own && own.status === "confirmed" && cancel !== null && cancel.visible ? (
        <div className="chip-actions">
          <form action={memberCancelBookingAction}>
            <ScheduleReturnFields returnTo={returnTo} />
            <input type="hidden" name="id" value={own.id} />
            <button className="ghost" type="submit">
              {cancel.label}
            </button>
          </form>
        </div>
      ) : null}
    </article>
  );
}
