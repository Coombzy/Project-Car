import {
  parseApiError,
  SESSION_COOKIE,
  shopApiUrl,
  type Principal,
  type WaitlistEntry,
} from "./config";
import { extractSessionValue, readSessionToken } from "./session";

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
  let response: Response;
  try {
    response = await shopFetch("/me");
  } catch {
    throw parseApiError(503, null, `Cannot reach shop API at ${shopApiUrl()}.`);
  }
  const body = await readJson(response);
  if (!response.ok) {
    throw parseApiError(response.status, body, "Could not load the current owner.");
  }
  return body as Principal;
}

export async function listWaitlist(): Promise<WaitlistEntry[]> {
  let response: Response;
  try {
    response = await shopFetch("/waitlist");
  } catch {
    throw parseApiError(503, null, `Cannot reach shop API at ${shopApiUrl()}.`);
  }
  const body = await readJson(response);
  if (!response.ok) {
    throw parseApiError(response.status, body, "Could not load the waitlist.");
  }
  return body as WaitlistEntry[];
}
