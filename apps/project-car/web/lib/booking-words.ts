/** Plain words for the booking calendar. Bay colours stay on existing CSS variables. */

export const TIME_LABEL = "Mountain Time";

export const PEAK_HOURS_PER_WEEK = 4;

export const TAKEN_MESSAGE = "That hour was just taken. Pick another time.";

export const BELOW_ZERO_MESSAGE = "That would take your balance below zero.";

export const AFTER_START_MESSAGE = "This visit has started, so it can't be cancelled here.";

export const NO_BAY_FREE_MESSAGE = "No bay is free for that whole time.";

export const CELL_WORD = {
  open: "Open",
  booked: "Booked",
  held: "Held",
  yours: "Yours",
  closed: "Closed",
  past: "Past",
  picked: "Picked",
  ask: "Ask first",
} as const;

export type CellWord = (typeof CELL_WORD)[keyof typeof CELL_WORD];

const STATUS_LABEL = {
  pending: "Waiting",
  confirmed: "Booked",
  active: "In the bay",
  completed: "Finished",
  overdue: "Late",
  cancelled: "Cancelled",
} as const;

export type BookingStatusWord = keyof typeof STATUS_LABEL;

export function bookingStatusLabel(status: string): string {
  switch (status) {
    case "pending":
    case "confirmed":
    case "active":
    case "completed":
    case "overdue":
    case "cancelled":
      return STATUS_LABEL[status];
    default:
      return status.replaceAll("_", " ");
  }
}

export const BAND_SHORT = {
  weekday_day: "Day",
  weekday_eve: "Eve",
  weekend_fri_eve: "Peak",
  late_night: "Night",
} as const;

export type BandId = keyof typeof BAND_SHORT;

/** Runs only when `node --test` loads this file. A client bundle has no Node argv, so import returns. */
function proveBookingWords(): void {
  if (typeof process === "undefined" || !Array.isArray(process.argv)) {
    return;
  }
  const entry = process.argv[1];
  if (typeof entry !== "string" || !import.meta.url.endsWith(entry)) {
    return;
  }
  const problems: string[] = [];
  if (typeof TIME_LABEL === "undefined" || TIME_LABEL !== "Mountain Time") {
    problems.push("TIME_LABEL");
  }
  if (typeof PEAK_HOURS_PER_WEEK === "undefined" || PEAK_HOURS_PER_WEEK !== 4) {
    problems.push("PEAK_HOURS_PER_WEEK");
  }
  if (typeof CELL_WORD === "undefined" || CELL_WORD.open !== "Open" || CELL_WORD.ask !== "Ask first") {
    problems.push("CELL_WORD");
  }
  if (
    typeof BAND_SHORT === "undefined" ||
    BAND_SHORT.weekday_day !== "Day" ||
    BAND_SHORT.weekend_fri_eve !== "Peak" ||
    BAND_SHORT.late_night !== "Night"
  ) {
    problems.push("BAND_SHORT");
  }
  if (
    typeof TAKEN_MESSAGE === "undefined" ||
    TAKEN_MESSAGE !== "That hour was just taken. Pick another time." ||
    typeof BELOW_ZERO_MESSAGE === "undefined" ||
    BELOW_ZERO_MESSAGE !== "That would take your balance below zero." ||
    typeof AFTER_START_MESSAGE === "undefined" ||
    AFTER_START_MESSAGE !== "This visit has started, so it can't be cancelled here." ||
    typeof NO_BAY_FREE_MESSAGE === "undefined" ||
    NO_BAY_FREE_MESSAGE !== "No bay is free for that whole time."
  ) {
    problems.push("messages");
  }
  const known: Record<string, string> = {
    pending: "Waiting",
    confirmed: "Booked",
    active: "In the bay",
    completed: "Finished",
    overdue: "Late",
    cancelled: "Cancelled",
  };
  for (const status of Object.keys(known)) {
    if (bookingStatusLabel(status) !== known[status]) {
      problems.push(status);
    }
  }
  const unknown = ["no", "show"].join("_");
  if (bookingStatusLabel(unknown) !== "no show") {
    problems.push("unknown status");
  }
  if (problems.length > 0) {
    throw new Error(problems.join("; "));
  }
}

proveBookingWords();
