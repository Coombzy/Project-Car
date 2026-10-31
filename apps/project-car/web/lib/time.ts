const SHOP_TZ = "America/Regina";

export function shopClock(): Date {
  const frozen = process.env.NEXT_PUBLIC_SHOP_NOW || process.env.SHOP_NOW;
  if (frozen) {
    const date = new Date(frozen);
    if (!Number.isNaN(date.getTime())) {
      return date;
    }
  }
  return new Date();
}

export function formatShopDateTime(iso: string): string {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) {
    return iso;
  }
  return new Intl.DateTimeFormat("en-CA", {
    dateStyle: "medium",
    timeStyle: "short",
    timeZone: SHOP_TZ,
  }).format(date);
}

export function formatShopTime(iso: string): string {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) {
    return iso;
  }
  return new Intl.DateTimeFormat("en-CA", {
    hour: "numeric",
    minute: "2-digit",
    timeZone: SHOP_TZ,
  }).format(date);
}

export function formatShopDate(iso: string): string {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) {
    return iso;
  }
  return new Intl.DateTimeFormat("en-CA", {
    weekday: "short",
    month: "short",
    day: "numeric",
    timeZone: SHOP_TZ,
  }).format(date);
}

export function shopTodayIso(): string {
  return new Intl.DateTimeFormat("en-CA", {
    timeZone: SHOP_TZ,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(shopClock());
}

export function addDays(isoDate: string, days: number): string {
  const [year, month, day] = isoDate.split("-").map(Number);
  const utc = new Date(Date.UTC(year, month - 1, day + days));
  const yyyy = utc.getUTCFullYear();
  const mm = String(utc.getUTCMonth() + 1).padStart(2, "0");
  const dd = String(utc.getUTCDate()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd}`;
}

export function mondayOf(isoDate: string): string {
  const [year, month, day] = isoDate.split("-").map(Number);
  const utc = new Date(Date.UTC(year, month - 1, day));
  const weekday = utc.getUTCDay(); // 0 Sun
  const offset = weekday === 0 ? -6 : 1 - weekday;
  return addDays(isoDate, offset);
}

function isRealCalendarDate(isoDate: string): boolean {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(isoDate);
  if (!match) {
    return false;
  }
  const year = Number(match[1]);
  const month = Number(match[2]);
  const day = Number(match[3]);
  // Date.UTC rolls 2026-02-31 to 3 March, and maps years 0-99 to 1900-1999.
  // setUTCFullYear pins the parsed year (it does not remap 0-99) before the round trip.
  const utc = new Date(Date.UTC(year, month - 1, day));
  utc.setUTCFullYear(year, month - 1, day);
  return utc.getUTCFullYear() === year && utc.getUTCMonth() === month - 1 && utc.getUTCDate() === day;
}

export function parseWeekParam(week?: string): string {
  if (week && isRealCalendarDate(week)) {
    return mondayOf(week);
  }
  return mondayOf(shopTodayIso());
}

export function weekdayLabel(isoDate: string): string {
  const [year, month, day] = isoDate.split("-").map(Number);
  const utc = new Date(Date.UTC(year, month - 1, day));
  return new Intl.DateTimeFormat("en-CA", {
    weekday: "short",
    month: "short",
    day: "numeric",
    timeZone: "UTC",
  }).format(utc);
}

export function tokensLabel(value: string | number): string {
  const amount = typeof value === "number" ? value : Number(value);
  if (Number.isNaN(amount)) {
    return String(value);
  }
  return Number.isInteger(amount) ? String(amount) : amount.toFixed(2);
}

export function overlayIsNonStandard(multiplier: string | number | undefined): boolean {
  if (multiplier === undefined) {
    return false;
  }
  return Number(multiplier) !== 1;
}

export function fillApplies(multiplier: string | number | undefined): boolean {
  if (multiplier === undefined) {
    return false;
  }
  return Number(multiplier) !== 1;
}

const DAY_START_HOUR = 10;

function shopParts(date: Date): { date: string; hour: number; minute: number; second: number } {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: SHOP_TZ,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hourCycle: "h23",
  }).formatToParts(date);
  const lookup = Object.fromEntries(parts.map((part) => [part.type, part.value]));
  return {
    date: `${lookup.year}-${lookup.month}-${lookup.day}`,
    hour: Number(lookup.hour),
    minute: Number(lookup.minute),
    second: Number(lookup.second),
  };
}

function hourStamp(date: string, hour: number): string {
  return `${date}T${String(hour).padStart(2, "0")}:00`;
}

export function defaultVisitWindow(now: Date = shopClock()): { start: string; end: string } {
  const parts = shopParts(now);
  let hour = parts.hour;
  let date = parts.date;
  if (parts.minute !== 0 || parts.second !== 0) {
    hour += 1;
  }
  if (hour < DAY_START_HOUR) {
    hour = DAY_START_HOUR;
  }
  if (hour >= 24) {
    date = addDays(date, 1);
    hour = DAY_START_HOUR;
  }
  const endHour = hour + 1;
  const endDate = endHour >= 24 ? addDays(date, 1) : date;
  return { start: hourStamp(date, hour), end: hourStamp(endDate, endHour % 24) };
}

function snapWholeHour(value: string): string {
  const match = /^(\d{4}-\d{2}-\d{2})T(\d{2}):(\d{2})(?::(\d{2}))?/.exec(value);
  if (!match) {
    return value;
  }
  let date = match[1];
  let hour = Number(match[2]);
  const minute = Number(match[3]);
  const second = Number(match[4] ?? "0");
  if (minute === 0 && second === 0) {
    return hourStamp(date, hour);
  }
  hour += 1;
  if (hour >= 24) {
    date = addDays(date, 1);
    hour = 0;
  }
  return hourStamp(date, hour);
}

export function snapWholeHourWindow(start: string, end: string): { start: string; end: string } {
  return { start: snapWholeHour(start), end: snapWholeHour(end) };
}

export function bayOptionLabel(hoist: { name: string; status: string; is_shop?: boolean }): string {
  const status = hoist.status === "occupied" ? "available" : hoist.status;
  const shop = hoist.is_shop ? " · shop hoist · request" : "";
  return `${hoist.name}${shop} · ${status}`;
}

export function shopDateTimeLocal(date: Date = shopClock()): string {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: SHOP_TZ,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    hourCycle: "h23",
  }).formatToParts(date);
  const lookup = Object.fromEntries(parts.map((part) => [part.type, part.value]));
  return `${lookup.year}-${lookup.month}-${lookup.day}T${lookup.hour}:${lookup.minute}`;
}
