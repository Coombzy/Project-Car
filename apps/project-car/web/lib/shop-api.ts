import {
  MEMBER_SESSION_COOKIE,
  parseApiError,
  SESSION_COOKIE,
  shopApiUrl,
  type Booking,
  type BookingQuote,
  type CalendarStatus,
  type ChatMessage,
  type ChatMessagePage,
  type ChatRoom,
  type Dashboard,
  type FillNotifyResult,
  type FillPreview,
  type Hoist,
  type Member,
  type MemberDashboard,
  type MemberDetail,
  type MemberSchedule,
  type MemberSelf,
  type MembershipTier,
  type NotificationOutbox,
  type Principal,
  type Todo,
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

export async function listTodos(): Promise<Todo[]> {
  return shopJson<Todo[]>("/todos", "Could not load to-dos.");
}

export async function createTodo(payload: Record<string, unknown>): Promise<Todo> {
  return shopJson<Todo>("/todos", "Could not create the to-do.", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export async function patchTodo(id: string, payload: Record<string, unknown>): Promise<Todo> {
  return shopJson<Todo>(`/todos/${id}`, "Could not update the to-do.", {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export async function deleteTodo(id: string): Promise<void> {
  let response: Response;
  try {
    response = await shopFetch(`/todos/${id}`, { method: "DELETE" });
  } catch {
    throw parseApiError(503, null, `Cannot reach shop API at ${shopApiUrl()}.`);
  }
  if (response.status === 204) {
    return;
  }
  const body = await readJson(response);
  throw parseApiError(response.status, body, "Could not delete the to-do.");
}

export async function downloadTodoIcs(id: string): Promise<{ filename: string; body: string }> {
  let response: Response;
  try {
    response = await shopFetch(`/todos/${id}/ics`);
  } catch {
    throw parseApiError(503, null, `Cannot reach shop API at ${shopApiUrl()}.`);
  }
  if (!response.ok) {
    const body = await readJson(response);
    throw parseApiError(response.status, body, "Could not download the calendar file.");
  }
  const disposition = response.headers.get("content-disposition") ?? "";
  const match = disposition.match(/filename="([^"]+)"/);
  return { filename: match?.[1] ?? `todo-${id}.ics`, body: await response.text() };
}

export async function getCalendarStatus(): Promise<CalendarStatus> {
  return shopJson<CalendarStatus>("/calendar/status", "Could not load calendar status.");
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

export async function previewFill(discountPct?: string): Promise<FillPreview> {
  const query = new URLSearchParams();
  if (discountPct) query.set("discount_pct", discountPct);
  const suffix = query.size ? `?${query.toString()}` : "";
  return shopJson<FillPreview>(`/fill/preview${suffix}`, "Could not preview next-day openings.");
}

export async function listFillOutbox(): Promise<NotificationOutbox[]> {
  return shopJson<NotificationOutbox[]>("/fill/outbox", "Could not load the notification outbox.");
}

export async function notifyFill(payload: {
  dry_run: boolean;
  discount_pct?: string;
  channels: string[];
}): Promise<FillNotifyResult> {
  return shopJson<FillNotifyResult>("/fill/notify", "Could not queue fill notifications.", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export async function listChatRooms(): Promise<ChatRoom[]> {
  return shopJson<ChatRoom[]>("/chat/rooms", "Could not load chat rooms.");
}

export async function getChatRoom(id: string): Promise<ChatRoom> {
  return shopJson<ChatRoom>(`/chat/rooms/${id}`, "Could not load that chat room.");
}

export async function createChatRoom(payload: { title: string; member_ids: string[] }): Promise<ChatRoom> {
  return shopJson<ChatRoom>("/chat/rooms", "Could not create the chat room.", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export async function muteChatRoom(id: string, muted: boolean): Promise<ChatRoom> {
  return shopJson<ChatRoom>(`/chat/rooms/${id}/mute`, "Could not update mute.", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ muted }),
  });
}

export async function listChatMessages(id: string, afterId?: string): Promise<ChatMessagePage> {
  const query = new URLSearchParams();
  if (afterId) query.set("after_id", afterId);
  const suffix = query.size ? `?${query.toString()}` : "";
  return shopJson<ChatMessagePage>(`/chat/rooms/${id}/messages${suffix}`, "Could not load chat messages.");
}

export async function postChatMessage(id: string, body: string): Promise<ChatMessage> {
  return shopJson<ChatMessage>(`/chat/rooms/${id}/messages`, "Could not send the message.", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ body }),
  });
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

export async function getMemberDashboard(): Promise<MemberDashboard> {
  return memberJson<MemberDashboard>("/member/dashboard", "Could not load your dashboard.");
}

export async function listMemberTodos(): Promise<Todo[]> {
  return memberJson<Todo[]>("/todos", "Could not load to-dos.");
}

export async function createMemberTodo(payload: Record<string, unknown>): Promise<Todo> {
  return memberJson<Todo>("/todos", "Could not create the to-do.", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export async function patchMemberTodo(id: string, payload: Record<string, unknown>): Promise<Todo> {
  return memberJson<Todo>(`/todos/${id}`, "Could not update the to-do.", {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export async function deleteMemberTodo(id: string): Promise<void> {
  let response: Response;
  try {
    response = await memberFetch(`/todos/${id}`, { method: "DELETE" });
  } catch {
    throw parseApiError(503, null, `Cannot reach shop API at ${shopApiUrl()}.`);
  }
  if (response.status === 204) {
    return;
  }
  const body = await readJson(response);
  throw parseApiError(response.status, body, "Could not delete the to-do.");
}

export async function downloadMemberTodoIcs(id: string): Promise<{ filename: string; body: string }> {
  let response: Response;
  try {
    response = await memberFetch(`/todos/${id}/ics`);
  } catch {
    throw parseApiError(503, null, `Cannot reach shop API at ${shopApiUrl()}.`);
  }
  if (!response.ok) {
    const body = await readJson(response);
    throw parseApiError(response.status, body, "Could not download the calendar file.");
  }
  const disposition = response.headers.get("content-disposition") ?? "";
  const match = disposition.match(/filename="([^"]+)"/);
  return { filename: match?.[1] ?? `todo-${id}.ics`, body: await response.text() };
}

export async function getMemberPrincipal(): Promise<Principal> {
  return memberJson<Principal>("/me", "Could not load the current member.");
}

export async function listMemberHoists(): Promise<Hoist[]> {
  return memberJson<Hoist[]>("/member/hoists", "Could not load customer bays.");
}


export async function getMemberFill(): Promise<FillPreview> {
  return memberJson<FillPreview>("/member/fill", "Could not load tomorrow's fill openings.");
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

export async function listMemberChatRooms(): Promise<ChatRoom[]> {
  return memberJson<ChatRoom[]>("/member/chat/rooms", "Could not load your chat rooms.");
}

export async function getMemberChatRoom(id: string): Promise<ChatRoom> {
  return memberJson<ChatRoom>(`/member/chat/rooms/${id}`, "Could not load that chat room.");
}

export async function listMemberChatMessages(id: string, afterId?: string): Promise<ChatMessagePage> {
  const query = new URLSearchParams();
  if (afterId) query.set("after_id", afterId);
  const suffix = query.size ? `?${query.toString()}` : "";
  return memberJson<ChatMessagePage>(
    `/member/chat/rooms/${id}/messages${suffix}`,
    "Could not load chat messages.",
  );
}

export async function postMemberChatMessage(id: string, body: string): Promise<ChatMessage> {
  return memberJson<ChatMessage>(`/member/chat/rooms/${id}/messages`, "Could not send the message.", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ body }),
  });
}
