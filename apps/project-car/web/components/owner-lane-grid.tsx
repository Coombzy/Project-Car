import Link from "next/link";

import { bandAt } from "../lib/booking-calendar";
import { TIME_LABEL, bookingStatusLabel } from "../lib/booking-words";
import type { RateHour } from "../lib/rate-chart";
import { addDays, parseShopInstant, scheduleHref, zonedDateTime } from "../lib/calendar";
import type { Booking, Hoist } from "../lib/config";
import { weekdayLabel } from "../lib/time";
import { OwnerBookingCard } from "./owner-booking-card";
import type { ScheduleReturn } from "./schedule-return-fields";

const OCCUPYING = new Set(["pending", "confirmed", "active", "completed", "overdue", "no_show"]);

function pad(hour: number): string {
  return String(hour).padStart(2, "0");
}

function bayNumber(hoist: Hoist): number {
  if (hoist.is_shop) {
    return 6;
  }
  const match = hoist.name.match(/(\d+)/);
  return match ? Number(match[1]) : 99;
}

function covers(booking: Booking, day: string, hour: number): boolean {
  const start = zonedDateTime(day, hour).getTime();
  const end = hour === 23 ? zonedDateTime(addDays(day, 1), 0).getTime() : zonedDateTime(day, hour + 1).getTime();
  return parseShopInstant(booking.start_at).getTime() < end && parseShopInstant(booking.end_at).getTime() > start;
}

function onDay(booking: Booking, day: string): boolean {
  const start = zonedDateTime(day, 0).getTime();
  const end = zonedDateTime(addDays(day, 1), 0).getTime();
  return parseShopInstant(booking.start_at).getTime() < end && parseShopInstant(booking.end_at).getTime() > start;
}

export function OwnerLaneGrid({
  days,
  nowIso,
  focusDay,
  hoists,
  bookings,
  returnTo,
  weekStart,
  month,
  saved,
}: {
  days: string[];
  nowIso: string;
  focusDay: string;
  hoists: Hoist[];
  bookings: Booking[];
  returnTo: ScheduleReturn;
  weekStart: string;
  month: string;
  saved?: readonly RateHour[];
}) {
  const now = parseShopInstant(nowIso).getTime();
  const hours = Array.from({ length: 18 }, (_, index) => index + 6);
  const phoneBookings = bookings.filter((booking) => onDay(booking, focusDay));

  return (
    <div className="owner-lanes">
      <style>{OWNER_LANE_CSS}</style>
      <p className="lede">
        Times are {TIME_LABEL}. A phone lists the day. A wide screen shows the week.
      </p>
      <div className="day-pills">
        {days.map((day) => (
          <Link
            key={day}
            href={scheduleHref("/schedule", { view: "week", week: weekStart, month, slot: undefined }) + `&day=${day}`}
            aria-current={day === focusDay ? "page" : undefined}
          >
            {weekdayLabel(day)}
          </Link>
        ))}
      </div>
      <div className="owner-list">
        {hoists.map((hoist) => {
          const rows = phoneBookings.filter((booking) => booking.hoist_id === hoist.id);
          return (
            <section key={hoist.id} className="card">
              <h2>
                {hoist.is_shop ? "Shop hoist" : hoist.name}
                {hoist.is_shop ? " — ask first" : ""}
              </h2>
              {rows.length === 0 ? (
                <p className="muted">Nothing booked this day.</p>
              ) : (
                rows.map((booking) => <OwnerBookingCard key={booking.id} booking={booking} returnTo={returnTo} />)
              )}
            </section>
          );
        })}
      </div>
      <div className="owner-grid" role="grid" aria-label={`Owner week, ${TIME_LABEL}`}>
        <div className="lane-row-hours">
          <div className="gutter" />
          {days.map((day) => (
            <div key={day} className="day-name">
              {weekdayLabel(day)}
            </div>
          ))}
        </div>
        {hours.map((hour) => (
          <div key={hour} className="lane-row-hours" role="row">
            <div className="gutter">{`${pad(hour)}:00`}</div>
            {days.map((day) => (
              <div key={day} className="day-bays">
                {hoists.map((hoist) => {
                  const booking = bookings.find(
                    (item) => item.hoist_id === hoist.id && OCCUPYING.has(item.status) && covers(item, day, hour),
                  );
                  const band = bandAt(day, hour, saved);
                  const past = zonedDateTime(day, hour).getTime() < now;
                  const text = booking
                    ? `${booking.member_name.split(" ")[0]} ${bookingStatusLabel(booking.status)}`
                    : hoist.status === "maintenance" || hoist.status === "locked"
                      ? "Closed"
                      : past
                        ? "Past"
                        : String(band.tokens);
                  return (
                    <div key={hoist.id} className={`lane-cell${booking ? " is-booked" : ""}`} role="gridcell">
                      {text}
                    </div>
                  );
                })}
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

const OWNER_LANE_CSS = `
.owner-lanes { display: flex; flex-direction: column; gap: 12px; }
.owner-lanes .day-pills { display: flex; flex-wrap: wrap; gap: 8px; }
.owner-lanes .day-pills a { min-height: 44px; display: inline-flex; align-items: center; padding: 0 8px; border: 1px solid var(--line); border-radius: 6px; }
.owner-list { display: flex; flex-direction: column; gap: 12px; }
.owner-grid { display: none; }
.owner-lanes .lane-row-hours { display: flex; gap: 4px; }
.owner-lanes .gutter { width: 3.5rem; flex: none; font-size: 13px; }
.owner-lanes .day-name, .owner-lanes .day-bays { flex: 1; min-width: 0; display: flex; gap: 2px; font-size: 13px; }
.owner-lanes .lane-cell { flex: 1; min-height: 28px; overflow: hidden; border-left: 3px solid var(--line); }
@media (min-width: 768px) {
  .owner-list { display: none; }
  .owner-grid { display: block; }
}
`;
