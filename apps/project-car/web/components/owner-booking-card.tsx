import { BookingCost } from "./booking-cost";
import { ScheduleReturnFields, type ScheduleReturn } from "./schedule-return-fields";
import { offersCancel } from "../lib/booking-cancel";
import { completeUnusedField } from "../lib/booking-complete";
import { bookingStatusLabel } from "../lib/booking-words";
import { formatCalendarTime } from "../lib/calendar";
import type { Booking } from "../lib/config";
import { checkInButtonState } from "../lib/check-in-window";
import { shopClock } from "../lib/time";
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
  const checkIn =
    booking.status === "confirmed" ? checkInButtonState(booking.start_at, shopClock(), booking.end_at) : null;
  const unused = completeUnusedField(booking.status, booking.reserved_tokens);
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
        {unused ? (
          <form className="complete-booking" action={completeBookingAction}>
            <ScheduleReturnFields returnTo={returnTo} />
            <input type="hidden" name="id" value={booking.id} />
            <label className="unused-tokens">
              Unused
              <input {...unused} inputMode="decimal" />
            </label>
            <button type="submit">Complete</button>
          </form>
        ) : null}
        {offersCancel(booking.status, "owner") ? (
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
