import { cookies } from "next/headers";

import { cookieSecure } from "./cookie-secure";
import { MEMBER_SESSION_COOKIE, SESSION_COOKIE } from "./config";
import { memberCookiePath } from "./member-cookie-path";

function extractNamedCookie(setCookieHeaders: string[], cookieName: string): string | null {
  for (const header of setCookieHeaders) {
    const pair = header.split(";", 1)[0] ?? "";
    const eq = pair.indexOf("=");
    if (eq === -1) {
      continue;
    }
    const name = pair.slice(0, eq).trim();
    if (name !== cookieName) {
      continue;
    }
    const raw = pair.slice(eq + 1).trim();
    try {
      return decodeURIComponent(raw);
    } catch {
      return raw;
    }
  }
  return null;
}

export function extractSessionValue(setCookieHeaders: string[]): string | null {
  return extractNamedCookie(setCookieHeaders, SESSION_COOKIE);
}

export function extractMemberSessionValue(setCookieHeaders: string[]): string | null {
  return extractNamedCookie(setCookieHeaders, MEMBER_SESSION_COOKIE);
}

async function readCookie(name: string): Promise<string | undefined> {
  const store = await cookies();
  return store.get(name)?.value;
}

async function writeCookie(name: string, value: string, maxAge = 86_400): Promise<void> {
  const store = await cookies();
  store.set({
    name,
    value,
    httpOnly: true,
    sameSite: "lax",
    secure: cookieSecure(),
    path: "/",
    maxAge,
  });
}

export async function readSessionToken(): Promise<string | undefined> {
  return readCookie(SESSION_COOKIE);
}

export async function writeSessionCookie(value: string, maxAge = 86_400): Promise<void> {
  await writeCookie(SESSION_COOKIE, value, maxAge);
}

export async function clearSessionCookie(): Promise<void> {
  const store = await cookies();
  store.delete(SESSION_COOKIE);
}

export async function readMemberSessionToken(): Promise<string | undefined> {
  return readCookie(MEMBER_SESSION_COOKIE);
}

export async function writeMemberSessionCookie(value: string, maxAge = 86_400): Promise<void> {
  const store = await cookies();
  store.set({
    name: MEMBER_SESSION_COOKIE,
    value,
    httpOnly: true,
    sameSite: "lax",
    secure: cookieSecure(),
    path: memberCookiePath(),
    maxAge,
  });
}

export async function clearMemberSessionCookie(): Promise<void> {
  const store = await cookies();
  store.delete({ name: MEMBER_SESSION_COOKIE, path: memberCookiePath() });
}
