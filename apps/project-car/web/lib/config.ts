export const SESSION_COOKIE = "pc_owner_session";
export const MEMBER_SESSION_COOKIE = "pc_member_session";

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
  member_id?: string | null;
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
  fill_id?: string;
  fill_label?: string;
  fill_multiplier?: string;
  fill_discount_pct?: string;
  hours: string;
  base_tokens: string;
  final_reserve_cost: string;
  tz: string;
};

export type FillGap = {
  hoist_id: string;
  hoist_name: string;
  start_at: string;
  end_at: string;
  hours: string;
};

export type FillPreview = {
  target_date: string;
  tz: string;
  window_start: string;
  window_end: string;
  bay_count: number;
  capacity_hours: string;
  booked_hours: string;
  open_hours: string;
  open_ratio: string;
  discount_pct: string;
  fill_multiplier: string;
  urgency: string;
  applies: boolean;
  gaps: FillGap[];
  offer_id: string | null;
  source: string;
};

export type NotificationOutbox = {
  id: string;
  channel: "email" | "sms" | "push";
  member_id: string | null;
  fill_offer_id: string | null;
  to_address: string | null;
  subject: string | null;
  body: string | null;
  payload: Record<string, unknown> | null;
  status: "pending" | "sent" | "failed" | "dry_run" | "skipped";
  attempts: number;
  last_error: string | null;
  dry_run: boolean;
  sent_at: string | null;
  created_at: string;
};

export type FillNotifyResult = {
  preview: FillPreview;
  dry_run: boolean;
  published: boolean;
  queued: number;
  notifications: NotificationOutbox[];
};

export type Booking = {
  id: string;
  member_id: string | null;
  member_name: string;
  hoist_id: string;
  hoist_name: string;
  kind: "customer" | "shop";
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
  is_shop: boolean;
  created_at: string;
  updated_at: string;
};

export type Occupancy = {
  booking_id: string;
  hoist_id: string;
  hoist_name: string;
  start_at: string;
  end_at: string;
  status: Booking["status"];
  own: boolean;
};

export type MemberSchedule = {
  hoists: Hoist[];
  bookings: Booking[];
  occupancy: Occupancy[];
};

export type MemberSelf = Member & {
  booking_window_days: number;
  max_simultaneous_bookings: number;
  included_tokens: number;
  bookings: Booking[];
  tokens: TokenTransaction[];
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

export type ChatParticipant = {
  member_id: string;
  name: string;
  email: string;
};

export type ChatMessage = {
  id: string;
  room_id: string;
  sender_role: "owner" | "member";
  sender_member_id: string | null;
  sender_email: string;
  sender_name: string;
  body: string;
  created_at: string;
};

export type ChatRoom = {
  id: string;
  title: string;
  muted: boolean;
  created_by_email: string;
  created_at: string;
  updated_at: string;
  participants: ChatParticipant[];
  last_message: ChatMessage | null;
  last_message_at: string | null;
};

export type ChatMessagePage = {
  messages: ChatMessage[];
  cursor: string | null;
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
