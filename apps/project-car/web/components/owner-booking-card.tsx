import {
  cancelBookingAction,
  checkInBookingAction,
  completeBookingAction,
  confirmBookingAction,
} from "../app/schedule/actions";
import { bookingStatusLabel } from "../lib/booking-words";
import { formatCalendarTime } from "../lib/calendar";
import { checkInButtonState } from "../lib/check-in-window";
import type { Booking } from "../lib/config";
import { shopClock } from "../lib/time";
import { BookingCost } from "./booking-cost";
import { ScheduleReturnFields, type ScheduleReturn } from "./schedule-return-fields";

export function OwnerBookingCard({
  booking,
  returnTo,
  compact,
}: {
  booking: Booking;
  returnTo: ScheduleReturn;
  compact?: boolean;
}) {
  const checkIn =
    booking.status === "confirmed" ? checkInButtonState(booking.start_at, shopClock(), booking.end_at) : null;
  return (
    <article
      className={`booking-chip status-${booking.status}${booking.kind === "shop" ? " booking-chip-shop" : ""}${compact ? " booking-chip-hour" : ""}`}
    >
      <strong>{booking.member_name}</strong>
      {booking.kind === "shop" ? <span className="pill pill-shop">Shop</span> : null}
      <div>
        {formatCalendarTime(booking.start_at)}–{formatCalendarTime(booking.end_at)} · Mountain Time
      </div>
      <BookingCost reservedTokens={booking.reserved_tokens} pricingRule={booking.pricing_rule} />
      <span className={`pill pill-${booking.status}`}>{bookingStatusLabel(booking.status)}</span>
      <div className="chip-actions">
        {booking.status === "pending" ? (
          <form action={confirmBookingAction}>
            <ScheduleReturnFields returnTo={returnTo} />
            <input type="hidden" name="id" value={booking.id} />
            <button type="submit">Confirm</button>
          </form>
        ) : null}
        {checkIn ? (
          <form action={checkInBookingAction}>
            <ScheduleReturnFields returnTo={returnTo} />
            <input type="hidden" name="id" value={booking.id} />
            <button type="submit" disabled={checkIn.disabled}>
              Check in
            </button>
            {checkIn.hint ? <span className="check-in-hint">{checkIn.hint}</span> : null}
          </form>
        ) : null}
        {booking.status === "active" || booking.status === "overdue" ? (
          <form className="complete-booking" action={completeBookingAction}>
            <ScheduleReturnFields returnTo={returnTo} />
            <input type="hidden" name="id" value={booking.id} />
            <button type="submit">Finish visit</button>
            <span className="check-in-hint">Time past the booked end is charged by the hour.</span>
          </form>
        ) : null}
        {booking.status === "pending" || booking.status === "confirmed" || booking.status === "active" ? (
          <form action={cancelBookingAction}>
            <ScheduleReturnFields returnTo={returnTo} />
            <input type="hidden" name="id" value={booking.id} />
            <label>
              Reason
              <input type="text" name="reason" required minLength={3} maxLength={500} />
            </label>
            <button className="ghost" type="submit">
              Cancel
            </button>
          </form>
        ) : null}
      </div>
    </article>
  );
}
