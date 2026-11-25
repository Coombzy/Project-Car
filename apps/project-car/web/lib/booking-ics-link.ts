export function icsHref(booking: { id: string; status: string }): string | null {
  if (booking.status !== "confirmed" && booking.status !== "pending") return null;
  return `/member/bookings/${encodeURIComponent(booking.id)}/ics`;
}
