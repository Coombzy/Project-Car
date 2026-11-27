export type ParsedTierForm =
  | {
      ok: true;
      name: string;
      display_name: string;
      price: string;
      included_tokens: number;
      booking_window_days: number;
      max_simultaneous_bookings: number;
      notes: string | null;
    }
  | { ok: false; error: string };

const NAME_RE = /^[a-z0-9][a-z0-9_-]{0,63}$/;

function text(value: unknown): string | null {
  return typeof value === "string" ? value : null;
}

function parsePrice(raw: string): string | null {
  const match = /^(\d+)(?:\.(\d+))?$/.exec(raw.trim());
  if (!match) return null;
  const whole = (match[1] ?? "").replace(/^0+(?=\d)/, "") || "0";
  const frac = (match[2] ?? "").replace(/0+$/, "");
  if (frac.length > 2) return null;
  const cents = Number(whole) * 100 + (frac ? Number(frac.padEnd(2, "0")) : 0);
  if (!Number.isSafeInteger(cents) || cents > 999_999) return null;
  return frac ? `${whole}.${frac}` : whole;
}

function wholeIn(raw: unknown, min: number, max: number): number | null {
  const value = text(raw)?.trim();
  if (value === undefined || !/^\d+$/.test(value)) return null;
  const n = Number(value);
  return Number.isSafeInteger(n) && n >= min && n <= max ? n : null;
}

export function parseTierForm(input: {
  name: unknown;
  display_name: unknown;
  price: unknown;
  included_tokens: unknown;
  booking_window_days: unknown;
  max_simultaneous_bookings: unknown;
  notes?: unknown;
}): ParsedTierForm {
  const name = text(input.name)?.trim().toLowerCase() ?? "";
  if (name === "pricing" || !NAME_RE.test(name)) {
    return { ok: false, error: "Enter a tier name (1-64 of a-z, 0-9, _ or -). pricing is reserved." };
  }
  const display_name = text(input.display_name)?.trim() ?? "";
  if (display_name.length < 1 || display_name.length > 120) {
    return { ok: false, error: "Enter a display name of 1-120 characters." };
  }
  const price = parsePrice(text(input.price) ?? "");
  if (price === null) {
    return { ok: false, error: "Price is 0 to 9999.99, with at most two decimal places." };
  }
  const included_tokens = wholeIn(input.included_tokens, 0, 100_000);
  const booking_window_days = wholeIn(input.booking_window_days, 1, 365);
  const max_simultaneous_bookings = wholeIn(input.max_simultaneous_bookings, 1, 20);
  if (included_tokens === null) {
    return { ok: false, error: "Included tokens must be a whole number from 0 to 100000." };
  }
  if (booking_window_days === null) {
    return { ok: false, error: "Booking window must be a whole number from 1 to 365." };
  }
  if (max_simultaneous_bookings === null) {
    return { ok: false, error: "Max simultaneous bookings must be a whole number from 1 to 20." };
  }
  return {
    ok: true,
    name,
    display_name,
    price,
    included_tokens,
    booking_window_days,
    max_simultaneous_bookings,
    notes: text(input.notes)?.trim() || null,
  };
}
