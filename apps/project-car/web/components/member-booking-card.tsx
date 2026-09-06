import { BookingCost } from "./booking-cost";
import { ScheduleReturnFields, type ScheduleReturn } from "./schedule-return-fields";
import { StatusPill } from "./status-pill";
import type { Booking, Occupancy } from "../lib/config";
import { formatCalendarTime } from "../lib/calendar";
import { memberCancelBookingAction, memberConfirmBookingAction } from "../app/member/schedule/actions";

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
  return (
    <article
      className={`booking-chip status-${slot.status}${slot.own ? "" : " occupancy-chip"}${compact ? " booking-chip-hour" : ""}`}
    >
      <strong>{slot.own ? "You" : "Booked"}</strong>
      <div>
        {formatCalendarTime(slot.start_at)}–{formatCalendarTime(slot.end_at)}
      </div>
      {own ? <BookingCost reservedTokens={own.reserved_tokens} pricingRule={own.pricing_rule} /> : null}
      <StatusPill value={slot.status} />
      {own && own.status === "pending" ? (
        <div className="chip-actions">
          <form action={memberConfirmBookingAction}>
            <ScheduleReturnFields returnTo={returnTo} />
            <input type="hidden" name="id" value={own.id} />
            <button type="submit">Confirm</button>
          </form>
          <form action={memberCancelBookingAction}>
            <ScheduleReturnFields returnTo={returnTo} />
            <input type="hidden" name="id" value={own.id} />
            <button className="ghost" type="submit">
              Cancel
            </button>
          </form>
        </div>
      ) : null}
      {own && (own.status === "confirmed" || own.status === "active") ? (
        <div className="chip-actions">
          <form action={memberCancelBookingAction}>
            <ScheduleReturnFields returnTo={returnTo} />
            <input type="hidden" name="id" value={own.id} />
            <button className="ghost" type="submit">
              Cancel
            </button>
          </form>
        </div>
      ) : null}
    </article>
  );
}
