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
  type JobEvent,
  type ShopHoistRequest,
  type Member,
  type MemberDashboard,
  type MemberDetail,
  type MemberSchedule,
  type MemberSelf,
  type MembershipTier,
  type NotificationOutbox,
  type PartsOrder,
  type PartsRequest,
  type Principal,
  type Todo,
  type TokenTransaction,
  type ToolCribEvent,
  type WaitlistEntry,
} from "./config";
import {
  extractMemberSessionValue,
  extractSessionValue,
  readMemberSessionToken,
  readSessionToken,
} from "./session";
import { pathSegment } from "./shop-path";

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
    signal: init.signal ?? AbortSignal.timeout(10_000),
  });
}

export async function shopJson<T>(path: string, fallback: string, init: RequestInit = {}): Promise<T> {
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

export async function loginOwner(
  email: string,
  password: string,
  forwardHeaders: Record<string, string> = {},
): Promise<string> {
  let response: Response;
  try {
    response = await fetch(`${shopApiUrl()}/auth/login`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        ...forwardHeaders,
      },
      body: JSON.stringify({ email, password }),
      cache: "no-store",
      signal: AbortSignal.timeout(10_000),
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

export async function listPartsRequests(): Promise<PartsRequest[]> {
  return shopJson<PartsRequest[]>("/parts-requests", "Could not load parts requests.");
}

export async function patchPartsRequest(
  id: string,
  status: "fulfilled" | "declined",
): Promise<PartsRequest> {
  return shopJson<PartsRequest>(`/parts-requests/${pathSegment(id)}`, "Could not update the parts request.", {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status }),
  });
}

export async function listPartsOrders(): Promise<PartsOrder[]> {
  return shopJson<PartsOrder[]>("/parts-orders", "Could not load parts orders.");
}

export async function patchPartsOrder(
  id: string,
  status: PartsOrder["status"],
): Promise<PartsOrder> {
  return shopJson<PartsOrder>(`/parts-orders/${pathSegment(id)}`, "Could not update the parts order.", {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status }),
  });
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
  return shopJson<Todo>(`/todos/${pathSegment(id)}`, "Could not update the to-do.", {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export async function deleteTodo(id: string): Promise<void> {
  await apiClient("owner").del(`/todos/${pathSegment(id)}`, "Could not delete the to-do.");
}

export async function downloadTodoIcs(id: string): Promise<{ filename: string; body: string }> {
  return apiClient("owner").download(`/todos/${pathSegment(id)}/ics`, "Could not download the calendar file.", `todo-${id}.ics`);
}

export async function getCalendarStatus(): Promise<CalendarStatus> {
  return shopJson<CalendarStatus>("/calendar/status", "Could not load calendar status.");
}

export async function listWaitlist(): Promise<WaitlistEntry[]> {
  return shopJson<WaitlistEntry[]>("/waitlist", "Could not load the waitlist.");
}

export async function markWaitlistContacted(id: string): Promise<WaitlistEntry> {
  return shopJson<WaitlistEntry>(`/waitlist/${pathSegment(id)}/contacted`, "Could not mark the entry contacted.", {
    method: "POST",
  });
}

export async function listTiers(): Promise<MembershipTier[]> {
  return shopJson<MembershipTier[]>("/tiers", "Could not load tiers.");
}

export async function patchTier(name: string, payload: Partial<MembershipTier>): Promise<MembershipTier> {
  return shopJson<MembershipTier>(`/tiers/${pathSegment(name)}`, "Could not update the tier.", {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export async function listMembers(): Promise<Member[]> {
  return shopJson<Member[]>("/members", "Could not load members.");
}

export async function listJobEvents(): Promise<JobEvent[]> {
  return shopJson<JobEvent[]>("/jobs/events", "Could not load job rows.");
}

export async function listToolCribEvents(): Promise<ToolCribEvent[]> {
  return shopJson<ToolCribEvent[]>("/tool-crib/events", "Could not load crib checkout rows.");
}

export async function checkoutCribTool(payload: {
  member_id: string;
  sku: string;
  note?: string;
}): Promise<ToolCribEvent> {
  return shopJson<ToolCribEvent>("/tool-crib/checkouts", "Could not store the tool checkout.", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export async function returnCribTool(payload: { sku: string; note?: string }): Promise<ToolCribEvent> {
  return shopJson<ToolCribEvent>("/tool-crib/returns", "Could not store the tool return.", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export async function getMember(id: string): Promise<MemberDetail> {
  return shopJson<MemberDetail>(`/members/${pathSegment(id)}`, "Could not load that member.");
}

export async function createMember(payload: Record<string, unknown>): Promise<Member> {
  return shopJson<Member>("/members", "Could not create the member.", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export async function patchMember(id: string, payload: Record<string, unknown>): Promise<Member> {
  return shopJson<Member>(`/members/${pathSegment(id)}`, "Could not update the member.", {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export async function listMemberTokens(id: string): Promise<TokenTransaction[]> {
  return shopJson<TokenTransaction[]>(`/members/${pathSegment(id)}/tokens`, "Could not load the token ledger.");
}

export async function adjustMemberTokens(id: string, amount: string, note: string): Promise<TokenTransaction> {
  return shopJson<TokenTransaction>(`/members/${pathSegment(id)}/tokens`, "Could not adjust tokens.", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ amount, note }),
  });
}

export async function rebuildMemberTokens(id: string): Promise<Member> {
  return shopJson<Member>(`/members/${pathSegment(id)}/tokens/rebuild`, "Could not rebuild the token balance.", {
    method: "POST",
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
  return shopJson<Hoist>(`/hoists/${pathSegment(id)}`, "Could not update the hoist.", {
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
  return shopJson<Booking>(`/bookings/${pathSegment(id)}/confirm`, "Could not confirm the booking.", { method: "POST" });
}

export async function checkInBooking(id: string): Promise<Booking> {
  return shopJson<Booking>(`/bookings/${pathSegment(id)}/check-in`, "Could not check in the booking.", { method: "POST" });
}

export async function completeBooking(id: string, unusedTokens = "0"): Promise<Booking> {
  return shopJson<Booking>(`/bookings/${pathSegment(id)}/complete`, "Could not complete the booking.", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ unused_tokens: unusedTokens }),
  });
}

export async function cancelBooking(id: string): Promise<Booking> {
  return shopJson<Booking>(`/bookings/${pathSegment(id)}/cancel`, "Could not cancel the booking.", { method: "POST" });
}

export async function listOwnerShopHoistRequests(
  status?: ShopHoistRequest["status"],
): Promise<ShopHoistRequest[]> {
  const query = new URLSearchParams();
  if (status) query.set("status", status);
  const suffix = query.size ? `?${query.toString()}` : "";
  return shopJson<ShopHoistRequest[]>(
    `/shop-hoist-requests${suffix}`,
    "Could not load shop hoist requests.",
  );
}

type ShopHoistDecision = {
  request_id: string;
  status: string;
  action: string;
  booking_id: string | null;
  token_balance: string | null;
};

export async function approveShopHoistRequest(id: string): Promise<ShopHoistDecision> {
  return shopJson<ShopHoistDecision>(
    `/shop-hoist-requests/${pathSegment(id)}/approve`,
    "Could not approve the shop hoist request.",
    { method: "POST" },
  );
}

export async function denyShopHoistRequest(id: string): Promise<ShopHoistDecision> {
  return shopJson<ShopHoistDecision>(
    `/shop-hoist-requests/${pathSegment(id)}/deny`,
    "Could not deny the shop hoist request.",
    { method: "POST" },
  );
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
  return shopJson<ChatRoom>(`/chat/rooms/${pathSegment(id)}`, "Could not load that chat room.");
}

export async function createChatRoom(payload: { title: string; member_ids: string[] }): Promise<ChatRoom> {
  return shopJson<ChatRoom>("/chat/rooms", "Could not create the chat room.", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export async function muteChatRoom(id: string, muted: boolean): Promise<ChatRoom> {
  return shopJson<ChatRoom>(`/chat/rooms/${pathSegment(id)}/mute`, "Could not update mute.", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ muted }),
  });
}

export async function listChatMessages(id: string, afterId?: string): Promise<ChatMessagePage> {
  const query = new URLSearchParams();
  if (afterId) query.set("after_id", afterId);
  const suffix = query.size ? `?${query.toString()}` : "";
  return shopJson<ChatMessagePage>(`/chat/rooms/${pathSegment(id)}/messages${suffix}`, "Could not load chat messages.");
}

export async function postChatMessage(id: string, body: string): Promise<ChatMessage> {
  return shopJson<ChatMessage>(`/chat/rooms/${pathSegment(id)}/messages`, "Could not send the message.", {
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
    signal: init.signal ?? AbortSignal.timeout(10_000),
  });
}

export async function memberJson<T>(path: string, fallback: string, init: RequestInit = {}): Promise<T> {
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

type ShopRealm = "owner" | "member";

async function realmCall(realm: ShopRealm, path: string, init?: RequestInit): Promise<Response> {
  const call = ({ owner: shopFetch, member: memberFetch } satisfies Record<ShopRealm, typeof shopFetch>)[realm];
  try {
    return await call(path, init);
  } catch {
    throw parseApiError(503, null, `Cannot reach shop API at ${shopApiUrl()}.`);
  }
}

export function apiClient(realm: ShopRealm) {
  const json = ({ owner: shopJson, member: memberJson } satisfies Record<ShopRealm, typeof shopJson>)[realm];
  const send = (method: "POST" | "PATCH", body?: unknown): RequestInit =>
    body === undefined ? { method } : { method, headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) };
  return {
    get: <T>(path: string, fallback: string) => json<T>(path, fallback),
    post: <T>(path: string, fallback: string, body?: unknown) => json<T>(path, fallback, send("POST", body)),
    patch: <T>(path: string, fallback: string, body?: unknown) => json<T>(path, fallback, send("PATCH", body)),
    async del(path: string, fallback: string): Promise<void> {
      const response = await realmCall(realm, path, { method: "DELETE" });
      if (response.status === 204) return;
      throw parseApiError(response.status, await readJson(response), fallback);
    },
    async download(path: string, fallback: string, filename: string) {
      const response = await realmCall(realm, path);
      if (!response.ok) throw parseApiError(response.status, await readJson(response), fallback);
      const match = (response.headers.get("content-disposition") ?? "").match(/filename="([^"]+)"/);
      return { filename: match?.[1] ?? filename, body: await response.text() };
    },
  };
}

export async function loginMember(
  email: string,
  password: string,
  forwardHeaders: Record<string, string> = {},
): Promise<string> {
  let response: Response;
  try {
    response = await fetch(`${shopApiUrl()}/auth/member/login`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        ...forwardHeaders,
      },
      body: JSON.stringify({ email, password }),
      cache: "no-store",
      signal: AbortSignal.timeout(10_000),
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

export async function listMemberPartsRequests(): Promise<PartsRequest[]> {
  return memberJson<PartsRequest[]>(
    "/member/parts-requests",
    "Could not load parts requests.",
  );
}

export async function createMemberPartsRequest(payload: {
  sku: string;
  note?: string;
}): Promise<PartsRequest> {
  return memberJson<PartsRequest>(
    "/member/parts-requests",
    "Could not store the parts request.",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    },
  );
}

export async function createMemberTodo(payload: Record<string, unknown>): Promise<Todo> {
  return memberJson<Todo>("/todos", "Could not create the to-do.", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export async function patchMemberTodo(id: string, payload: Record<string, unknown>): Promise<Todo> {
  return memberJson<Todo>(`/todos/${pathSegment(id)}`, "Could not update the to-do.", {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export async function deleteMemberTodo(id: string): Promise<void> {
  await apiClient("member").del(`/todos/${pathSegment(id)}`, "Could not delete the to-do.");
}

export async function downloadMemberTodoIcs(id: string): Promise<{ filename: string; body: string }> {
  return apiClient("member").download(`/todos/${pathSegment(id)}/ics`, "Could not download the calendar file.", `todo-${id}.ics`);
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

export async function getMemberShopHoist(): Promise<Hoist> {
  return memberJson<Hoist>("/member/shop-hoist", "Could not load the shop hoist.");
}

export async function requestMemberShopHoist(payload: Record<string, unknown>): Promise<ShopHoistRequest> {
  return memberJson<ShopHoistRequest>("/member/shop-hoist-requests", "Could not request the shop hoist.", {
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
  return memberJson<Booking>(`/member/bookings/${pathSegment(id)}/confirm`, "Could not confirm the booking.", {
    method: "POST",
  });
}

export async function cancelMemberBooking(id: string): Promise<Booking> {
  return memberJson<Booking>(`/member/bookings/${pathSegment(id)}/cancel`, "Could not cancel the booking.", {
    method: "POST",
  });
}

export async function downloadMemberBookingIcs(id: string): Promise<{ filename: string; body: string }> {
  let response: Response;
  try {
    response = await memberFetch(`/member/bookings/${pathSegment(id)}/ics`);
  } catch {
    throw parseApiError(503, null, `Cannot reach shop API at ${shopApiUrl()}.`);
  }
  if (!response.ok) {
    const body = await readJson(response);
    throw parseApiError(response.status, body, "Could not download the calendar file.");
  }
  const disposition = response.headers.get("content-disposition") ?? "";
  const match = disposition.match(/filename="([^"]+)"/);
  return { filename: match?.[1] ?? `booking-${id}.ics`, body: await response.text() };
}

export async function listMemberJobEvents(): Promise<JobEvent[]> {
  return memberJson<JobEvent[]>("/member/jobs/events", "Could not load job rows.");
}

export async function claimJob(payload: { job_key: string; note?: string }): Promise<JobEvent> {
  return memberJson<JobEvent>("/member/jobs/claims", "Could not store the job claim.", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export async function markJobDone(payload: { job_key: string; note?: string }): Promise<JobEvent> {
  return memberJson<JobEvent>("/member/jobs/done", "Could not store the job done row.", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

export async function listMemberChatRooms(): Promise<ChatRoom[]> {
  return memberJson<ChatRoom[]>("/member/chat/rooms", "Could not load your chat rooms.");
}

export async function getMemberChatRoom(id: string): Promise<ChatRoom> {
  return memberJson<ChatRoom>(`/member/chat/rooms/${pathSegment(id)}`, "Could not load that chat room.");
}

export async function listMemberChatMessages(id: string, afterId?: string): Promise<ChatMessagePage> {
  const query = new URLSearchParams();
  if (afterId) query.set("after_id", afterId);
  const suffix = query.size ? `?${query.toString()}` : "";
  return memberJson<ChatMessagePage>(
    `/member/chat/rooms/${pathSegment(id)}/messages${suffix}`,
    "Could not load chat messages.",
  );
}

export async function postMemberChatMessage(id: string, body: string): Promise<ChatMessage> {
  return memberJson<ChatMessage>(`/member/chat/rooms/${pathSegment(id)}/messages`, "Could not send the message.", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ body }),
  });
}
