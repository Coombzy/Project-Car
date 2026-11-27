import type { RateHour } from "./rate-chart";
import { BAND_SHORT, type BandId } from "./booking-words";

const BAND_MULTIPLIER: Record<BandId, number> = {
  weekday_day: 1,
  weekday_eve: 1.25,
  weekend_fri_eve: 1.5,
  late_night: 0.75,
};

const BASE_TOKENS = 100;
const PEAK_BAND: BandId = "weekend_fri_eve";

export type BandAt = {
  id: BandId;
  short: string;
  tokens: number;
  gutter: string;
  countsTowardPeakCap: boolean;
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
  } else if (weekday >= 5 || (weekday === 4 && hour >= 16)) {
    id = "weekend_fri_eve";
  } else if (hour >= 16) {
    id = "weekday_eve";
  }
  const tokens = BASE_TOKENS * BAND_MULTIPLIER[id];
  const short = BAND_SHORT[id];
  return { id, short, tokens, gutter: `${short} ${tokens}`, countsTowardPeakCap: id === PEAK_BAND };
}

/**
 * Member cancel on the schedule list.
 *
 * Pending and confirmed visits can be cancelled only before the start.
 * The shop refunds the whole reserve; this does not keep a share inside 24 hours.
 * Active and overdue visits have no cancel control.
 * Naive start times are America/Regina, which stays UTC−6 all year.
 */

export type CancelOffer = {
  visible: boolean;
  refund: number;
  kept: number;
  label: string;
};

const SHOP_OFFSET = "-06:00";

function cents(amount: string): number {
  const value = Number(amount);
  if (!Number.isFinite(value)) {
    return 0;
  }
  return Math.round(value * 100);
}

function fromCents(value: number): number {
  return value / 100;
}

function shopInstant(iso: string): number {
  if (/[zZ]|[+-]\d{2}:?\d{2}$/.test(iso)) {
    return new Date(iso).getTime();
  }
  const match = /^(\d{4}-\d{2}-\d{2})T(\d{2}):(\d{2})(?::(\d{2}))?/.exec(iso);
  if (!match) {
    return new Date(iso).getTime();
  }
  const seconds = match[4] ?? "00";
  return new Date(`${match[1]}T${match[2]}:${match[3]}:${seconds}${SHOP_OFFSET}`).getTime();
}

export function memberCancelOffer(
  booking: { status: string; startAt: string; reservedTokens: string },
  now: Date,
): CancelOffer {
  const reserved = fromCents(cents(booking.reservedTokens));
  const hidden: CancelOffer = {
    visible: false,
    refund: 0,
    kept: reserved,
    label: "",
  };
  if (booking.status !== "pending" && booking.status !== "confirmed") {
    return hidden;
  }
  const start = shopInstant(booking.startAt);
  if (!Number.isFinite(start) || now.getTime() >= start) {
    return hidden;
  }
  return {
    visible: true,
    refund: reserved,
    kept: 0,
    label: "Cancel",
  };
}

const OCCUPYING = new Set(["pending", "confirmed", "active", "overdue"]);

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

function rangesOverlap(start: number, end: number, otherStart: number, otherEnd: number): boolean {
  return start < otherEnd && otherStart < end;
}

export function submittedHoistId(laneHoistId: string, bayId: string): string {
  if (laneHoistId === "any") {
    return "";
  }
  return bayId;
}

export function lowestFreeBay(
  bays: BayChoice[],
  intervals: SpanInterval[],
  startAt: string,
  endAt: string,
): BayChoice | null {
  const start = shopInstant(startAt);
  const end = shopInstant(endAt);
  const ordered = [...bays]
    .filter((bay) => !bay.isShop && bay.status !== "maintenance" && bay.status !== "locked")
    .sort((a, b) => a.number - b.number);
  for (const bay of ordered) {
    const taken = intervals.some((interval) => {
      if (interval.hoistId !== bay.id || !OCCUPYING.has(interval.status)) {
        return false;
      }
      return rangesOverlap(start, end, shopInstant(interval.startAt), shopInstant(interval.endAt));
    });
    if (!taken) {
      return bay;
    }
  }
  return null;
}
