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
