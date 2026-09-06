import { BookingCost } from "./booking-cost";
import { ScheduleReturnFields, type ScheduleReturn } from "./schedule-return-fields";
import { StatusPill } from "./status-pill";
import type { Booking } from "../lib/config";
import { formatCalendarTime } from "../lib/calendar";
import {
  cancelBookingAction,
  checkInBookingAction,
  completeBookingAction,
  confirmBookingAction,
} from "../app/schedule/actions";

export function OwnerBookingCard({
  booking,
  returnTo,
  compact,
}: {
  booking: Booking;
  returnTo: ScheduleReturn;
  compact?: boolean;
}) {
  return (
    <article
      className={`booking-chip status-${booking.status}${booking.kind === "shop" ? " booking-chip-shop" : ""}${compact ? " booking-chip-hour" : ""}`}
    >
      <strong>{booking.member_name}</strong>
      {booking.kind === "shop" ? <StatusPill value="shop" /> : null}
      <div>
        {formatCalendarTime(booking.start_at)}–{formatCalendarTime(booking.end_at)}
      </div>
      <BookingCost reservedTokens={booking.reserved_tokens} pricingRule={booking.pricing_rule} />
      <StatusPill value={booking.status} />
      <div className="chip-actions">
        {booking.status === "pending" ? (
          <form action={confirmBookingAction}>
            <ScheduleReturnFields returnTo={returnTo} />
            <input type="hidden" name="id" value={booking.id} />
            <button type="submit">Confirm</button>
          </form>
        ) : null}
        {booking.status === "confirmed" ? (
          <form action={checkInBookingAction}>
            <ScheduleReturnFields returnTo={returnTo} />
            <input type="hidden" name="id" value={booking.id} />
            <button type="submit">Check in</button>
          </form>
        ) : null}
        {booking.status === "active" ? (
          <form action={completeBookingAction}>
            <ScheduleReturnFields returnTo={returnTo} />
            <input type="hidden" name="id" value={booking.id} />
            <input type="hidden" name="unused_tokens" value="0" />
            <button type="submit">Complete</button>
          </form>
        ) : null}
        {booking.status === "pending" || booking.status === "confirmed" || booking.status === "active" ? (
          <form action={cancelBookingAction}>
            <ScheduleReturnFields returnTo={returnTo} />
            <input type="hidden" name="id" value={booking.id} />
            <button className="ghost" type="submit">
              Cancel
            </button>
          </form>
        ) : null}
      </div>
    </article>
  );
}
