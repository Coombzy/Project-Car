import {
  MEMBER_SESSION_COOKIE,
  parseApiError,
  SESSION_COOKIE,
  shopApiUrl,
  type Booking,
  type BookingQuote,
  type Dashboard,
  type Hoist,
  type Member,
  type MemberDetail,
  type MemberSchedule,
  type MemberSelf,
  type MembershipTier,
  type Principal,
  type TokenTransaction,
  type WaitlistEntry,
} from "./config";
import {
  extractMemberSessionValue,
  extractSessionValue,
  readMemberSessionToken,
  readSessionToken,
} from "./session";

async function readJson(response: Response): Promise<unknown> {
  const text = await response.text();
  if (!text) {
    return null;
  }
  try {
    return JSON.parse(text) as unknown;
  } catch {
    return null;
  }
}

async function shopFetch(path: string, init: RequestInit = {}): Promise<Response> {
  const token = await readSessionToken();
  const headers = new Headers(init.headers);
  headers.set("Accept", "application/json");
  if (token && !headers.has("Cookie")) {
    headers.set("Cookie", `${SESSION_COOKIE}=${encodeURIComponent(token)}`);
  }
  return fetch(`${shopApiUrl()}${path}`, {
    ...init,
    headers,
    cache: "no-store",
  });
}

async function shopJson<T>(path: string, fallback: string, init: RequestInit = {}): Promise<T> {
  let response: Response;
  try {
    response = await shopFetch(path, init);
  } catch {
    throw parseApiError(503, null, `Cannot reach shop API at ${shopApiUrl()}.`);
  }
  const body = await readJson(response);
  if (!response.ok) {
    throw parseApiError(response.status, body, fallback);
  }
  return body as T;
}

export async function loginOwner(email: string, password: string): Promise<string> {
  let response: Response;
  try {
    response = await fetch(`${shopApiUrl()}/auth/login`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
      cache: "no-store",
    });
  } catch {
    throw parseApiError(503, null, `Cannot reach shop API at ${shopApiUrl()}.`);
  }

  const body = await readJson(response);
  if (!response.ok) {
    throw parseApiError(response.status, body, "Login failed.");
  }

  const token = extractSessionValue(response.headers.getSetCookie());
  if (!token) {
    throw parseApiError(502, null, "Shop API did not return an owner session cookie.");
  }
  return token;
}

export async function logoutOwner(): Promise<void> {
  try {
    await shopFetch("/auth/logout", { method: "POST" });
  } catch {
    // Cookie is cleared locally either way.
  }
}

export async function getMe(): Promise<Principal> {
  return shopJson<Principal>("/me", "Could not load the current owner.");
}

export async function getDashboard(): Promise<Dashboard> {
  return shopJson<Dashboard>("/dashboard", "Could not load the dashboard.");
}

export async function listWaitlist(): Promise<WaitlistEntry[]> {
  return shopJson<WaitlistEntry[]>("/waitlist", "Could not load the waitlist.");
}

export async function markWaitlistContacted(id: string): Promise<WaitlistEntry> {
  return shopJson<WaitlistEntry>(`/waitlist/${id}/contacted`, "Could not mark the entry contacted.", {
    method: "POST",
  });
}

export async function listTiers(): Promise<MembershipTier[]> {
  return shopJson<MembershipTier[]>("/tiers", "Could not load tiers.");
}

export async function patchTier(name: string, payload: Partial<MembershipTier>): Promise<MembershipTier> {
  return shopJson<MembershipTier>(`/tiers/${name}`, "Could not update the tier.", {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export async function listMembers(): Promise<Member[]> {
  return shopJson<Member[]>("/members", "Could not load members.");
}

export async function getMember(id: string): Promise<MemberDetail> {
  return shopJson<MemberDetail>(`/members/${id}`, "Could not load that member.");
}

export async function createMember(payload: Record<string, unknown>): Promise<Member> {
  return shopJson<Member>("/members", "Could not create the member.", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export async function patchMember(id: string, payload: Record<string, unknown>): Promise<Member> {
  return shopJson<Member>(`/members/${id}`, "Could not update the member.", {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export async function listMemberTokens(id: string): Promise<TokenTransaction[]> {
  return shopJson<TokenTransaction[]>(`/members/${id}/tokens`, "Could not load the token ledger.");
}

export async function adjustMemberTokens(id: string, amount: string, note: string): Promise<TokenTransaction> {
  return shopJson<TokenTransaction>(`/members/${id}/tokens`, "Could not adjust tokens.", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ amount, note }),
  });
}

export async function listHoists(): Promise<Hoist[]> {
  return shopJson<Hoist[]>("/hoists", "Could not load hoists.");
}

export async function createHoist(payload: Record<string, unknown>): Promise<Hoist> {
  return shopJson<Hoist>("/hoists", "Could not create the hoist.", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export async function patchHoist(id: string, payload: Record<string, unknown>): Promise<Hoist> {
  return shopJson<Hoist>(`/hoists/${id}`, "Could not update the hoist.", {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export async function listBookings(params?: {
  hoistId?: string;
  memberId?: string;
  windowStart?: string;
  windowEnd?: string;
}): Promise<Booking[]> {
  const query = new URLSearchParams();
  if (params?.hoistId) query.set("hoist_id", params.hoistId);
  if (params?.memberId) query.set("member_id", params.memberId);
  if (params?.windowStart) query.set("window_start", params.windowStart);
  if (params?.windowEnd) query.set("window_end", params.windowEnd);
  const suffix = query.size ? `?${query.toString()}` : "";
  return shopJson<Booking[]>(`/bookings${suffix}`, "Could not load bookings.");
}

export async function quoteBooking(payload: {
  start_at: string;
  end_at: string;
  member_id?: string;
}): Promise<BookingQuote> {
  return shopJson<BookingQuote>("/bookings/quote", "Could not quote the booking.", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export async function createBooking(payload: Record<string, unknown>): Promise<Booking> {
  return shopJson<Booking>("/bookings", "Could not create the booking.", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export async function confirmBooking(id: string): Promise<Booking> {
  return shopJson<Booking>(`/bookings/${id}/confirm`, "Could not confirm the booking.", { method: "POST" });
}

export async function checkInBooking(id: string): Promise<Booking> {
  return shopJson<Booking>(`/bookings/${id}/check-in`, "Could not check in the booking.", { method: "POST" });
}

export async function completeBooking(id: string, unusedTokens = "0"): Promise<Booking> {
  return shopJson<Booking>(`/bookings/${id}/complete`, "Could not complete the booking.", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ unused_tokens: unusedTokens }),
  });
}

export async function cancelBooking(id: string): Promise<Booking> {
  return shopJson<Booking>(`/bookings/${id}/cancel`, "Could not cancel the booking.", { method: "POST" });
}

async function memberFetch(path: string, init: RequestInit = {}): Promise<Response> {
  const token = await readMemberSessionToken();
  const headers = new Headers(init.headers);
  headers.set("Accept", "application/json");
  if (token && !headers.has("Cookie")) {
    headers.set("Cookie", `${MEMBER_SESSION_COOKIE}=${encodeURIComponent(token)}`);
  }
  return fetch(`${shopApiUrl()}${path}`, {
    ...init,
    headers,
    cache: "no-store",
  });
}

async function memberJson<T>(path: string, fallback: string, init: RequestInit = {}): Promise<T> {
  let response: Response;
  try {
    response = await memberFetch(path, init);
  } catch {
    throw parseApiError(503, null, `Cannot reach shop API at ${shopApiUrl()}.`);
  }
  const body = await readJson(response);
  if (!response.ok) {
    throw parseApiError(response.status, body, fallback);
  }
  return body as T;
}

export async function loginMember(email: string, password: string): Promise<string> {
  let response: Response;
  try {
    response = await fetch(`${shopApiUrl()}/auth/member/login`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
      cache: "no-store",
    });
  } catch {
    throw parseApiError(503, null, `Cannot reach shop API at ${shopApiUrl()}.`);
  }

  const body = await readJson(response);
  if (!response.ok) {
    throw parseApiError(response.status, body, "Login failed.");
  }

  const token = extractMemberSessionValue(response.headers.getSetCookie());
  if (!token) {
    throw parseApiError(502, null, "Shop API did not return a member session cookie.");
  }
  return token;
}

export async function logoutMember(): Promise<void> {
  try {
    await memberFetch("/auth/member/logout", { method: "POST" });
  } catch {
    // Cookie is cleared locally either way.
  }
}

export async function getMemberMe(): Promise<MemberSelf> {
  return memberJson<MemberSelf>("/member/me", "Could not load your member profile.");
}

export async function getMemberPrincipal(): Promise<Principal> {
  return memberJson<Principal>("/me", "Could not load the current member.");
}

export async function listMemberHoists(): Promise<Hoist[]> {
  return memberJson<Hoist[]>("/member/hoists", "Could not load customer bays.");
}

export async function listMemberTokens(): Promise<TokenTransaction[]> {
  return memberJson<TokenTransaction[]>("/member/tokens", "Could not load your token ledger.");
}

export async function getMemberSchedule(params?: {
  windowStart?: string;
  windowEnd?: string;
}): Promise<MemberSchedule> {
  const query = new URLSearchParams();
  if (params?.windowStart) query.set("window_start", params.windowStart);
  if (params?.windowEnd) query.set("window_end", params.windowEnd);
  const suffix = query.size ? `?${query.toString()}` : "";
  return memberJson<MemberSchedule>(`/member/schedule${suffix}`, "Could not load your schedule.");
}

export async function quoteMemberBooking(payload: {
  start_at: string;
  end_at: string;
}): Promise<BookingQuote> {
  return memberJson<BookingQuote>("/member/bookings/quote", "Could not quote the booking.", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export async function createMemberBooking(payload: Record<string, unknown>): Promise<Booking> {
  return memberJson<Booking>("/member/bookings", "Could not create the booking.", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export async function confirmMemberBooking(id: string): Promise<Booking> {
  return memberJson<Booking>(`/member/bookings/${id}/confirm`, "Could not confirm the booking.", {
    method: "POST",
  });
}

export async function cancelMemberBooking(id: string): Promise<Booking> {
  return memberJson<Booking>(`/member/bookings/${id}/cancel`, "Could not cancel the booking.", {
    method: "POST",
  });
}
