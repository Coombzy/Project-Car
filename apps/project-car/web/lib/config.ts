export const SESSION_COOKIE = "pc_owner_session";

export function shopApiUrl(): string {
  const raw = process.env.SHOP_API_URL ?? "http://127.0.0.1:8000";
  return raw.replace(/\/$/, "");
}

export type ApiErrorBody = {
  error?: {
    code?: string;
    message?: string;
  };
};

export type Principal = {
  role: string;
  email: string;
};

export type WaitlistEntry = {
  id: string;
  name: string;
  email: string;
  phone: string | null;
  notes: string | null;
  contacted_at: string | null;
  created_at: string;
};

export type MembershipTier = {
  name: string;
  display_name: string;
  price: string;
  included_tokens: number;
  booking_window_days: number;
  max_simultaneous_bookings: number;
  notes: string | null;
  created_at: string;
  updated_at: string;
};

export type Member = {
  id: string;
  name: string;
  email: string;
  phone: string | null;
  tier_name: string;
  status: "active" | "suspended" | "banned" | "churned";
  waiver_signed_at: string | null;
  waiver_version: string | null;
  emergency_contact_name: string | null;
  emergency_contact_phone: string | null;
  token_balance: string;
  deposit_balance: string;
  created_at: string;
  updated_at: string;
};

export type PricingRule = {
  band_id: string;
  band_label: string;
  band_multiplier: string;
  overlay_id: string;
  overlay_label: string;
  advance_multiplier: string;
  hours: string;
  base_tokens: string;
  final_reserve_cost: string;
  tz: string;
};

export type Booking = {
  id: string;
  member_id: string;
  member_name: string;
  hoist_id: string;
  hoist_name: string;
  start_at: string;
  end_at: string;
  status: "pending" | "confirmed" | "active" | "completed" | "overdue" | "cancelled";
  reserved_tokens: string;
  pricing_rule: PricingRule | null;
  notes: string | null;
  created_at: string;
  updated_at: string;
};

export type BookingQuote = {
  pricing_rule: PricingRule;
  reserved_tokens: string;
  token_balance: string | null;
  token_balance_after: string | null;
};

export type MemberDetail = Member & {
  bookings: Booking[];
};

export type TokenTransaction = {
  id: string;
  member_id: string;
  booking_id: string | null;
  kind: string;
  amount: string;
  note: string | null;
  meta: { pricing_rule?: PricingRule } | null;
  created_at: string;
};

export type Hoist = {
  id: string;
  name: string;
  location_label: string;
  status: "available" | "occupied" | "maintenance" | "locked";
  created_at: string;
  updated_at: string;
};

export type HoistSnapshot = Hoist & {
  current_booking: Booking | null;
};

export type MemberAtRisk = {
  id: string;
  name: string;
  email: string;
  tier_name: string;
  token_balance: string;
};

export type Dashboard = {
  hoists: HoistSnapshot[];
  today_bookings: Booking[];
  waitlist_count: number;
  token_at_risk: MemberAtRisk[];
};

export class ShopApiError extends Error {
  readonly status: number;
  readonly code: string;

  constructor(status: number, code: string, message: string) {
    super(message);
    this.name = "ShopApiError";
    this.status = status;
    this.code = code;
  }
}

export function parseApiError(status: number, body: unknown, fallback: string): ShopApiError {
  const parsed = body as ApiErrorBody;
  const code = parsed?.error?.code ?? "http_error";
  const message = parsed?.error?.message ?? fallback;
  return new ShopApiError(status, code, message);
}
