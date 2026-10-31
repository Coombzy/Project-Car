import { addDays, calendarDate, parseShopInstant, zonedDateTime } from "./calendar";
import type { RateHour } from "./rate-chart";
import {
  AFTER_START_MESSAGE,
  BAND_SHORT,
  BELOW_ZERO_MESSAGE,
  PEAK_HOURS_PER_WEEK,
  TAKEN_MESSAGE,
  type BandId,
} from "./booking-words";

/** Seeded band table from the shop API. A quote at Book is the price that is charged. */
const BAND_MULTIPLIER: Record<BandId, number> = {
  weekday_day: 1,
  weekday_eve: 1.25,
  weekend_fri_eve: 1.5,
  late_night: 0.75,
};

const BASE_TOKENS = 100;
const PHONE_MAX_PX = 767;
const FREE_CANCEL_MS = 24 * 60 * 60 * 1000;
const LATE_KEEP_PCT = 50;
const PEAK_BAND: BandId = "weekend_fri_eve";

const OCCUPYING = new Set(["pending", "confirmed", "active", "completed", "overdue"]);

export type SavedBands = {
  hours: readonly RateHour[];
  peakCapHours: number;
};

export type BandAt = {
  id: BandId;
  short: string;
  tokens: number;
  gutter: string;
  countsTowardPeakCap: boolean;
};

export type BayChoice = {
  id: string;
  name: string;
  number: number;
  isShop: boolean;
  status: string;
};

export type SpanInterval = {
  hoistId: string;
  startAt: string;
  endAt: string;
  status: string;
};

export type SelectionSummary = {
  hours: number[];
  line: string;
  note: string | null;
  total: number;
};

export type CancelOffer = {
  visible: boolean;
  refund: number;
  kept: number;
  label: string;
  confirmText: string;
  note: string;
};

export type PeakUsage = {
  cap: number;
  used: number;
  remaining: number;
  line: string;
};

export type PurchaseMeta = {
  subtotal_cad?: string;
  gst_rate?: string;
  gst_cad?: string;
  total_cad?: string;
};

function pad(hour: number): string {
  return String(hour).padStart(2, "0");
}

function weekdayIndex(isoDate: string): number {
  const [year, month, day] = isoDate.split("-").map(Number);
  const utc = new Date(Date.UTC(year, month - 1, day)).getUTCDay();
  return utc === 0 ? 6 : utc - 1;
}

function isBandId(value: string): value is BandId {
  return value in BAND_SHORT;
}

export function bandAt(isoDate: string, hour: number, saved?: readonly RateHour[]): BandAt {
  const weekday = weekdayIndex(isoDate);
  const row = saved?.find((item) => item.weekday === weekday && item.hour === hour);
  if (row && isBandId(row.band_id)) {
    const tokens = Number(row.tokens_per_hour);
    const short = BAND_SHORT[row.band_id];
    const shown = Number.isInteger(tokens) ? String(tokens) : row.tokens_per_hour;
    return {
      id: row.band_id,
      short,
      tokens,
      gutter: `${short} ${shown}`,
      countsTowardPeakCap: row.counts_toward_peak_cap,
    };
  }
  let id: BandId = "weekday_day";
  if (hour >= 21 || hour < 8) {
    id = "late_night";
  } else if (hour >= 16) {
    id = "weekday_eve";
  } else if (weekday >= 5) {
    id = "weekend_fri_eve";
  }
  const tokens = BASE_TOKENS * BAND_MULTIPLIER[id];
  const short = BAND_SHORT[id];
  return { id, short, tokens, gutter: `${short} ${tokens}`, countsTowardPeakCap: id === PEAK_BAND };
}

export type QuotedHour = {
  band_label: string;
  band_tokens: string;
};

export function quotedSelectionLine(
  rule:
    | {
        segments?: QuotedHour[];
        final_reserve_cost?: string;
        fill_multiplier?: string;
        fill_label?: string;
      }
    | null
    | undefined,
): string | null {
  if (!rule?.final_reserve_cost || !rule.segments || rule.segments.length === 0) {
    return null;
  }
  const groups: { label: string; tokens: string; count: number }[] = [];
  for (const segment of rule.segments) {
    const last = groups[groups.length - 1];
    if (last && last.label === segment.band_label && last.tokens === segment.band_tokens) {
      last.count += 1;
    } else {
      groups.push({ label: segment.band_label, tokens: segment.band_tokens, count: 1 });
    }
  }
  const parts = groups.map((group) => {
    const subtotal = Number(group.tokens) * group.count;
    const shown = Number.isInteger(subtotal) ? String(subtotal) : subtotal.toFixed(2);
    return `${group.label} ${group.tokens} × ${group.count} = ${shown}`;
  });
  const fill =
    rule.fill_multiplier && Number(rule.fill_multiplier) !== 1 && rule.fill_label ? ` · ${rule.fill_label}` : "";
  return `${parts.join(" · ")}${fill} · Total ${rule.final_reserve_cost}`;
}

export function selectionSummary(
  isoDate: string,
  startHour: number,
  endHour: number,
  blocked: ReadonlySet<number> = new Set(),
  saved?: readonly RateHour[],
): SelectionSummary {
  const hours: number[] = [];
  let note: string | null = null;
  const lo = Math.min(startHour, endHour);
  const hi = Math.max(startHour, endHour);
  for (let hour = lo; hour < hi; hour += 1) {
    if (blocked.has(hour)) {
      note = `${pad(hour)}:00 is booked; selection ends at ${pad(hour)}:00`;
      break;
    }
    hours.push(hour);
  }
  const groups: { short: string; tokens: number; count: number }[] = [];
  for (const hour of hours) {
    const band = bandAt(isoDate, hour, saved);
    const last = groups[groups.length - 1];
    if (last && last.short === band.short && last.tokens === band.tokens) {
      last.count += 1;
    } else {
      groups.push({ short: band.short, tokens: band.tokens, count: 1 });
    }
  }
  const total = groups.reduce((sum, group) => sum + group.tokens * group.count, 0);
  const parts = groups.map((group) => `${group.short} ${group.tokens} × ${group.count} = ${group.tokens * group.count}`);
  const line = parts.length === 0 ? "" : `${parts.join(" · ")} · Total ${total}`;
  return { hours, line, note, total };
}

function rangesOverlap(start: number, end: number, otherStart: number, otherEnd: number): boolean {
  return start < otherEnd && otherStart < end;
}

export function lowestFreeBay(
  bays: BayChoice[],
  intervals: SpanInterval[],
  startAt: string,
  endAt: string,
): BayChoice | null {
  const start = parseShopInstant(startAt).getTime();
  const end = parseShopInstant(endAt).getTime();
  const ordered = [...bays].filter((bay) => !bay.isShop && bay.status === "available").sort((a, b) => a.number - b.number);
  for (const bay of ordered) {
    const taken = intervals.some((interval) => {
      if (interval.hoistId !== bay.id || !OCCUPYING.has(interval.status)) {
        return false;
      }
      return rangesOverlap(
        start,
        end,
        parseShopInstant(interval.startAt).getTime(),
        parseShopInstant(interval.endAt).getTime(),
      );
    });
    if (!taken) {
      return bay;
    }
  }
  return null;
}

function cents(amount: string | number): number {
  return Math.round(Number(amount) * 100);
}

function fromCents(value: number): number {
  return value / 100;
}

function keepCents(reservedCents: number, pct: number): number {
  return Math.floor((reservedCents * pct + 50) / 100);
}

export function memberCancelOffer(
  booking: { status: string; startAt: string; reservedTokens: string },
  now: Date,
): CancelOffer {
  const start = parseShopInstant(booking.startAt).getTime();
  const reserved = fromCents(cents(booking.reservedTokens));
  const hidden: CancelOffer = {
    visible: false,
    refund: 0,
    kept: reserved,
    label: "",
    confirmText: "",
    note: AFTER_START_MESSAGE,
  };
  if (booking.status === "active" || booking.status === "no_show" || booking.status === "completed" || booking.status === "cancelled" || booking.status === "overdue") {
    return hidden;
  }
  if (booking.status !== "pending" && booking.status !== "confirmed") {
    return hidden;
  }
  if (now.getTime() >= start) {
    return hidden;
  }
  const lead = start - now.getTime();
  const reservedCents = cents(booking.reservedTokens);
  const kept = lead >= FREE_CANCEL_MS ? 0 : fromCents(keepCents(reservedCents, LATE_KEEP_PCT));
  const refund = fromCents(reservedCents - keepCents(reservedCents, lead >= FREE_CANCEL_MS ? 0 : LATE_KEEP_PCT));
  const refundText = Number.isInteger(refund) ? String(refund) : refund.toFixed(2);
  return {
    visible: true,
    refund,
    kept,
    label: `Cancel · get ${refundText} tokens back`,
    confirmText: `Cancel this visit? You get ${refundText} tokens back.`,
    note: lead >= FREE_CANCEL_MS ? "Free to cancel until 24 hours before it starts." : "Late cancel keeps half.",
  };
}

function hourInZone(instant: Date): number {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: "America/Regina",
    hour: "2-digit",
    hourCycle: "h23",
  }).formatToParts(instant);
  const hour = parts.find((part) => part.type === "hour")?.value ?? "0";
  return Number(hour);
}

export function peakWeek(
  bookings: { status: string; startAt: string; endAt: string }[],
  weekStart: string,
  saved?: SavedBands,
): PeakUsage {
  const cap = saved?.peakCapHours ?? PEAK_HOURS_PER_WEEK;
  const weekBegin = zonedDateTime(weekStart, 0).getTime();
  const weekEnd = zonedDateTime(addDays(weekStart, 7), 0).getTime();
  let used = 0;
  for (const booking of bookings) {
    if (booking.status === "cancelled") {
      continue;
    }
    let cursor = parseShopInstant(booking.startAt).getTime();
    const end = parseShopInstant(booking.endAt).getTime();
    while (cursor < end) {
      if (cursor >= weekBegin && cursor < weekEnd) {
        const instant = new Date(cursor);
        const band = bandAt(calendarDate(instant.toISOString()), hourInZone(instant), saved?.hours);
        if (band.countsTowardPeakCap) {
          used += 1;
        }
      }
      cursor += 3_600_000;
    }
  }
  const remaining = Math.max(0, cap - used);
  return {
    cap,
    used,
    remaining,
    line: `Peak hours this week: ${used} used · ${remaining} left`,
  };
}

export function gstLine(meta: { purchase?: PurchaseMeta; pricing_rule?: unknown } | null | undefined): string | null {
  const purchase = meta?.purchase;
  if (!purchase?.gst_cad || !purchase.subtotal_cad || !purchase.total_cad) {
    return null;
  }
  return `Subtotal $${purchase.subtotal_cad} · GST $${purchase.gst_cad} · total $${purchase.total_cad}`;
}

export function bookingErrorCopy(code: string, fallback: string): string {
  switch (code) {
    case "hoist_overlap":
      return TAKEN_MESSAGE;
    case "would_go_negative":
      return BELOW_ZERO_MESSAGE;
    case "cancel_after_start":
      return AFTER_START_MESSAGE;
    case "peak_cap":
      return fallback;
    case "price_changed":
      return "The price changed. Nothing was booked.";
    default:
      return fallback;
  }
}

export function calendarViewForWidth(width: number): "day" | "week" {
  return width <= PHONE_MAX_PX ? "day" : "week";
}

export function balanceWouldGoNegative(balance: string | number, cost: number): boolean {
  return Number(balance) - cost < 0;
}
