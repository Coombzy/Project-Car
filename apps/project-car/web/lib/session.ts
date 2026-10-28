import { cookies } from "next/headers";

import { cookieSecure } from "./cookie-secure";
import { MEMBER_SESSION_COOKIE, SESSION_COOKIE } from "./config";
import { memberCookiePath } from "./member-cookie-path";

export {
  extractNamedCookie,
  extractSessionValue,
  extractMemberSessionValue,
} from "./session-cookie";

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
  store.delete({
    name: SESSION_COOKIE,
    path: "/",
    secure: cookieSecure(),
  });
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
  store.delete({
    name: MEMBER_SESSION_COOKIE,
    path: memberCookiePath(),
    secure: cookieSecure(),
  });
}
