/**
 * Shop calendar helpers (America/Regina).
 *
 * Monthly heat-map density is booked hours vs open shop hours (08:00–21:00).
 * Weekly hour slots are shop-local America/Regina. Cancelled bookings do not
 * occupy a hoist. Naive Owner `datetime-local` values still go through the
 * existing API helper (America/Edmonton); during Mountain Daylight both
 * zones are UTC−6.
 */

export const CALENDAR_TZ = "America/Regina";
export const OPEN_HOUR_START = 8;
export const OPEN_HOUR_END = 21;
export const OPEN_SHOP_HOURS = OPEN_HOUR_END - OPEN_HOUR_START;
export const DAY_HOURS = 24;

export type DensityLevel = "empty" | "light" | "medium" | "heavy" | "full";
export type ScheduleView = "month" | "week";

export type CalendarInterval = {
  hoist_id: string;
  start_at: string;
  end_at: string;
  status: string;
};

const OCCUPYING_STATUSES = new Set(["pending", "confirmed", "active", "completed", "overdue"]);

export function isOccupyingStatus(status: string): boolean {
  return OCCUPYING_STATUSES.has(status);
}

export function densityLevel(bookedHours: number, openHours: number = OPEN_SHOP_HOURS): DensityLevel {
  if (!Number.isFinite(bookedHours) || bookedHours <= 0 || openHours <= 0) {
    return "empty";
  }
  const ratio = bookedHours / openHours;
  if (ratio >= 0.75) {
    return "full";
  }
  if (ratio >= 0.5) {
    return "heavy";
  }
  if (ratio >= 0.25) {
    return "medium";
  }
  return "light";
}

export function parseShopInstant(iso: string, timeZone: string = CALENDAR_TZ): Date {
  if (/[zZ]|[+-]\d{2}:?\d{2}$/.test(iso)) {
    return new Date(iso);
  }
  const match = iso.match(/^(\d{4}-\d{2}-\d{2})T(\d{2}):(\d{2})(?::(\d{2}))?/);
  if (match) {
    return zonedDateTime(match[1], Number(match[2]), Number(match[3] ?? "0"), timeZone);
  }
  return new Date(iso);
}

export function calendarDate(iso: string, timeZone: string = CALENDAR_TZ): string {
  const date = parseShopInstant(iso, timeZone);
  if (Number.isNaN(date.getTime())) {
    return iso.slice(0, 10);
  }
  return new Intl.DateTimeFormat("en-CA", {
    timeZone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(date);
}

export function calendarTodayIso(now: Date = new Date()): string {
  return new Intl.DateTimeFormat("en-CA", {
    timeZone: CALENDAR_TZ,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(now);
}

export function formatCalendarTime(iso: string): string {
  const date = parseShopInstant(iso);
  if (Number.isNaN(date.getTime())) {
    return iso;
  }
  return new Intl.DateTimeFormat("en-CA", {
    hour: "numeric",
    minute: "2-digit",
    timeZone: CALENDAR_TZ,
  }).format(date);
}

export function formatMonthLabel(monthIso: string): string {
  const [year, month] = monthIso.split("-").map(Number);
  const utc = new Date(Date.UTC(year, month - 1, 1));
  return new Intl.DateTimeFormat("en-CA", {
    month: "long",
    year: "numeric",
    timeZone: "UTC",
  }).format(utc);
}

export function monthOf(isoDate: string): string {
  return isoDate.slice(0, 7);
}

export function addMonths(monthIso: string, delta: number): string {
  const [year, month] = monthIso.split("-").map(Number);
  const utc = new Date(Date.UTC(year, month - 1 + delta, 1));
  const yyyy = utc.getUTCFullYear();
  const mm = String(utc.getUTCMonth() + 1).padStart(2, "0");
  return `${yyyy}-${mm}`;
}

export function parseMonthParam(month?: string, today: string = calendarTodayIso()): string {
  if (month && /^\d{4}-\d{2}$/.test(month)) {
    const [, mm] = month.split("-").map(Number);
    if (mm >= 1 && mm <= 12) {
      return month;
    }
  }
  return monthOf(today);
}

export function parseViewParam(view?: string, week?: string): ScheduleView {
  if (view === "month") {
    return "month";
  }
  if (view === "week" || (Boolean(week) && !view)) {
    return "week";
  }
  return "month";
}

export function parseHoistParam(hoist?: string): string | undefined {
  if (hoist && /^[0-9a-f-]{36}$/i.test(hoist)) {
    return hoist;
  }
  return undefined;
}

export function monthGrid(monthIso: string): string[][] {
  const first = `${monthIso}-01`;
  const start = mondayOf(first);
  const nextMonth = addMonths(monthIso, 1);
  const weeks: string[][] = [];
  let cursor = start;
  while (weeks.length === 0 || monthOf(cursor) !== nextMonth) {
    const week = Array.from({ length: 7 }, (_, index) => addDays(cursor, index));
    weeks.push(week);
    cursor = addDays(cursor, 7);
    if (weeks.length >= 6) {
      break;
    }
  }
  return weeks;
}

export function monthWindow(monthIso: string): { start: string; end: string } {
  const weeks = monthGrid(monthIso);
  const first = weeks[0]?.[0];
  const last = weeks[weeks.length - 1]?.[6];
  if (!first || !last) {
    return { start: `${monthIso}-01`, end: `${addMonths(monthIso, 1)}-01` };
  }
  return { start: first, end: addDays(last, 1) };
}

export function addDays(isoDate: string, days: number): string {
  const [year, month, day] = isoDate.split("-").map(Number);
  const utc = new Date(Date.UTC(year, month - 1, day + days));
  return `${utc.getUTCFullYear()}-${pad(utc.getUTCMonth() + 1)}-${pad(utc.getUTCDate())}`;
}

export function mondayOf(isoDate: string): string {
  const [year, month, day] = isoDate.split("-").map(Number);
  const weekday = new Date(Date.UTC(year, month - 1, day)).getUTCDay();
  const offset = weekday === 0 ? -6 : 1 - weekday;
  return addDays(isoDate, offset);
}

function pad(value: number): string {
  return String(value).padStart(2, "0");
}

function tzOffsetMs(instant: Date, timeZone: string): number {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hourCycle: "h23",
  }).formatToParts(instant);
  const lookup = Object.fromEntries(parts.map((part) => [part.type, part.value]));
  const asUtc = Date.UTC(
    Number(lookup.year),
    Number(lookup.month) - 1,
    Number(lookup.day),
    Number(lookup.hour),
    Number(lookup.minute),
    Number(lookup.second),
  );
  return asUtc - instant.getTime();
}

/** Instant for a Regina (or other zone) wall clock on a calendar date. */
export function zonedDateTime(isoDate: string, hour = 0, minute = 0, timeZone: string = CALENDAR_TZ): Date {
  const [year, month, day] = isoDate.split("-").map(Number);
  const wallAsUtc = Date.UTC(year, month - 1, day, hour, minute, 0);
  const first = new Date(wallAsUtc - tzOffsetMs(new Date(wallAsUtc), timeZone));
  return new Date(wallAsUtc - tzOffsetMs(first, timeZone));
}

export function overlapHours(startIso: string, endIso: string, windowStart: Date, windowEnd: Date): number {
  const start = parseShopInstant(startIso).getTime();
  const end = parseShopInstant(endIso).getTime();
  if (Number.isNaN(start) || Number.isNaN(end) || end <= start) {
    return 0;
  }
  const left = Math.max(start, windowStart.getTime());
  const right = Math.min(end, windowEnd.getTime());
  if (right <= left) {
    return 0;
  }
  return (right - left) / 3_600_000;
}

export function bookedHoursOnDay(
  intervals: CalendarInterval[],
  hoistId: string,
  dayIso: string,
  timeZone: string = CALENDAR_TZ,
): number {
  const dayStart = zonedDateTime(dayIso, 0, 0, timeZone);
  const dayEnd = zonedDateTime(addDays(dayIso, 1), 0, 0, timeZone);
  return intervals
    .filter((interval) => interval.hoist_id === hoistId && isOccupyingStatus(interval.status))
    .reduce((sum, interval) => sum + overlapHours(interval.start_at, interval.end_at, dayStart, dayEnd), 0);
}

export function hoistDayDensity(
  intervals: CalendarInterval[],
  hoistId: string,
  dayIso: string,
  openHours: number = OPEN_SHOP_HOURS,
  timeZone: string = CALENDAR_TZ,
): { bookedHours: number; level: DensityLevel; ratio: number } {
  const bookedHours = bookedHoursOnDay(intervals, hoistId, dayIso, timeZone);
  return {
    bookedHours,
    level: densityLevel(bookedHours, openHours),
    ratio: openHours > 0 ? bookedHours / openHours : 0,
  };
}

export type HourPlacement = {
  day: string;
  topPct: number;
  heightPct: number;
  startHour: number;
  endHour: number;
};

export function bookingHourPlacement(
  startIso: string,
  endIso: string,
  dayIso: string,
  timeZone: string = CALENDAR_TZ,
): HourPlacement | null {
  const dayStart = zonedDateTime(dayIso, 0, 0, timeZone);
  const dayEnd = zonedDateTime(addDays(dayIso, 1), 0, 0, timeZone);
  const hours = overlapHours(startIso, endIso, dayStart, dayEnd);
  if (hours <= 0) {
    return null;
  }
  const start = Math.max(parseShopInstant(startIso).getTime(), dayStart.getTime());
  const end = Math.min(parseShopInstant(endIso).getTime(), dayEnd.getTime());
  const startHour = (start - dayStart.getTime()) / 3_600_000;
  const endHour = (end - dayStart.getTime()) / 3_600_000;
  const heightHours = Math.max(endHour - startHour, 0.25);
  return {
    day: dayIso,
    topPct: (startHour / DAY_HOURS) * 100,
    heightPct: (heightHours / DAY_HOURS) * 100,
    startHour,
    endHour,
  };
}

export function hourLabels(startHour = 0, endHour = DAY_HOURS): string[] {
  return Array.from({ length: endHour - startHour }, (_, index) => {
    const hour = startHour + index;
    return `${pad(hour)}:00`;
  });
}

export function hoistChipLabel(name: string, isShop: boolean): string {
  if (isShop) {
    return "Shop";
  }
  const match = name.match(/(\d+)/);
  return match ? `B${match[1]}` : name.slice(0, 3);
}

export function sortHoists<T extends { name: string; is_shop: boolean }>(hoists: T[]): T[] {
  return [...hoists].sort((left, right) => {
    if (left.is_shop !== right.is_shop) {
      return left.is_shop ? 1 : -1;
    }
    return left.name.localeCompare(right.name);
  });
}

export function scheduleHref(
  base: "/schedule" | "/member/schedule",
  params: {
    view?: ScheduleView;
    week?: string;
    month?: string;
    hoist?: string;
    slot?: string;
    error?: string;
  },
): string {
  const query = new URLSearchParams();
  if (params.view) {
    query.set("view", params.view);
  }
  if (params.week) {
    query.set("week", params.week);
  }
  if (params.month) {
    query.set("month", params.month);
  }
  if (params.hoist) {
    query.set("hoist", params.hoist);
  }
  if (params.slot) {
    query.set("slot", params.slot);
  }
  if (params.error) {
    query.set("error", params.error);
  }
  const suffix = query.size ? `?${query.toString()}` : "";
  const hash = params.slot ? "#create-booking" : "";
  return `${base}${suffix}${hash}`;
}

export function parseSlotParam(slot?: string): string | undefined {
  if (slot && /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/.test(slot)) {
    return slot;
  }
  return undefined;
}

export function slotEnd(slot: string): string {
  const [date, time] = slot.split("T");
  const [hour, minute] = time.split(":").map(Number);
  const next = zonedDateTime(date, hour, minute);
  next.setTime(next.getTime() + 60 * 60 * 1000);
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: CALENDAR_TZ,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    hourCycle: "h23",
  }).formatToParts(next);
  const lookup = Object.fromEntries(parts.map((part) => [part.type, part.value]));
  return `${lookup.year}-${lookup.month}-${lookup.day}T${lookup.hour}:${lookup.minute}`;
}

export function naiveWindow(isoDate: string, hour = 0): string {
  return `${isoDate}T${pad(hour)}:00:00`;
}
