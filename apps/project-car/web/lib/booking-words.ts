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
  no_show: "No-show",
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
    case "no_show":
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
