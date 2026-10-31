/**
 * Next visit for the member home.
 *
 * A booking is eligible when it is not cancelled and has not ended
 * (`end_at` is still after `now`). A visit that has already started is
 * still the next visit until that end. The earliest start wins.
 * Check-in opens 15 minutes before start, the R31 stand-in
 * (`CHECK_IN_EARLY_MINUTES` in `lib/check-in-window.ts` and the shop API).
 * Day and time are America/Regina.
 */

const SHOP_TZ = "America/Regina";

export const NEXT_VISIT_EARLY_MINUTES = 15;

export const NO_VISIT_BOOKED = "No visit booked";

export const SCHEDULE_HREF = "/member/schedule";

export type NextVisitBooking = {
  id: string;
  hoist_name: string;
  start_at: string;
  end_at: string;
  status: string;
};

export type NextVisit = {
  id: string;
  bay: string;
  status: string;
  dayLabel: string;
  timeLabel: string;
  opensAt: string;
  checkInOpensLabel: string;
};

function instant(iso: string): number {
  return new Date(iso).getTime();
}

function shopDay(date: Date): string {
  return new Intl.DateTimeFormat("en-CA", {
    weekday: "short",
    month: "short",
    day: "numeric",
    timeZone: SHOP_TZ,
  }).format(date);
}

function hourMinute(date: Date): string {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: SHOP_TZ,
    hour: "2-digit",
    minute: "2-digit",
    hourCycle: "h23",
  }).formatToParts(date);
  const hour = parts.find((part) => part.type === "hour")?.value;
  const minute = parts.find((part) => part.type === "minute")?.value;
  if (!hour || !minute) {
    return "";
  }
  return `${hour}:${minute}`;
}

export function checkInOpensAt(startAt: string, earlyMinutes: number = NEXT_VISIT_EARLY_MINUTES): Date {
  return new Date(instant(startAt) - earlyMinutes * 60 * 1000);
}

export function nextVisit(bookings: readonly NextVisitBooking[], now: Date): NextVisit | null {
  const nowMs = now.getTime();
  const eligible = bookings.filter((booking) => {
    if (booking.status === "cancelled") {
      return false;
    }
    const startMs = instant(booking.start_at);
    const endMs = instant(booking.end_at);
    if (!Number.isFinite(startMs) || !Number.isFinite(endMs)) {
      return false;
    }
    return endMs > nowMs;
  });
  eligible.sort((left, right) => {
    const byStart = instant(left.start_at) - instant(right.start_at);
    if (byStart !== 0) {
      return byStart;
    }
    const byEnd = instant(left.end_at) - instant(right.end_at);
    if (byEnd !== 0) {
      return byEnd;
    }
    if (left.id < right.id) {
      return -1;
    }
    if (left.id > right.id) {
      return 1;
    }
    return 0;
  });
  const booking = eligible[0];
  if (!booking) {
    return null;
  }
  const start = new Date(instant(booking.start_at));
  const end = new Date(instant(booking.end_at));
  const opens = checkInOpensAt(booking.start_at);
  return {
    id: booking.id,
    bay: booking.hoist_name,
    status: booking.status,
    dayLabel: shopDay(start),
    timeLabel: `${hourMinute(start)}\u2013${hourMinute(end)}`,
    opensAt: opens.toISOString(),
    checkInOpensLabel: `Check-in opens at ${hourMinute(opens)}`,
  };
}
