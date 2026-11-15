/** Plain status words for a member visit. Bay colours stay on the existing pill classes. */

const STATUS_LABEL = {
  pending: "Waiting",
  confirmed: "Booked",
  active: "In the bay",
  completed: "Finished",
  overdue: "Late",
  cancelled: "Cancelled",
} as const;

export type BookingStatusWord = keyof typeof STATUS_LABEL;

export function bookingStatusLabel(status: BookingStatusWord): string {
  switch (status) {
    case "pending":
    case "confirmed":
    case "active":
    case "completed":
    case "overdue":
    case "cancelled":
      return STATUS_LABEL[status];
    default: {
      const neverStatus: never = status;
      return neverStatus;
    }
  }
}
