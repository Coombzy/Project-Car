/**
 * Login `next` stays on this host.
 * Keep a value only when it starts with one `/`, contains no backslash,
 * and every percent-decoding of it still does. Owner falls back to `/`.
 * Member falls back to `/member` unless the path is `/member` or `/member/...`.
 */

const OWNER_FALLBACK = "/";
const MEMBER_FALLBACK = "/member";
const SAME_ORIGIN_BASE = "https://shop.invalid";
const CONTROL_CHARS = /[\u0000-\u001F\u007F]/;

function decodeChain(value: string): string[] | null {
  const chain = [value];
  let current = value;
  for (let i = 0; i < 5; i += 1) {
    if (!current.includes("%")) {
      return chain;
    }
    let decoded: string;
    try {
      decoded = decodeURIComponent(current);
    } catch {
      return null;
    }
    if (decoded === current) {
      return chain;
    }
    chain.push(decoded);
    current = decoded;
  }
  return null;
}

function isSameOriginRelative(value: string): boolean {
  if (!value.startsWith("/") || value.startsWith("//")) {
    return false;
  }
  if (value.includes("\\") || CONTROL_CHARS.test(value)) {
    return false;
  }
  let url: URL;
  try {
    url = new URL(value, SAME_ORIGIN_BASE);
  } catch {
    return false;
  }
  if (url.origin !== SAME_ORIGIN_BASE) {
    return false;
  }
  return url.pathname.startsWith("/") && !url.pathname.startsWith("//");
}

function pathnameOf(value: string): string | null {
  try {
    return new URL(value, SAME_ORIGIN_BASE).pathname;
  } catch {
    return null;
  }
}

function isMemberArea(pathname: string): boolean {
  return pathname === "/member" || pathname.startsWith("/member/");
}

export function safeOwnerNext(next: string | null | undefined): string {
  if (!next) {
    return OWNER_FALLBACK;
  }
  const chain = decodeChain(next);
  if (!chain || !chain.every(isSameOriginRelative)) {
    return OWNER_FALLBACK;
  }
  return next;
}

export function safeMemberNext(next: string | null | undefined): string {
  if (!next) {
    return MEMBER_FALLBACK;
  }
  const chain = decodeChain(next);
  if (!chain || !chain.every(isSameOriginRelative)) {
    return MEMBER_FALLBACK;
  }
  for (const variant of chain) {
    const pathname = pathnameOf(variant);
    if (pathname == null || !isMemberArea(pathname)) {
      return MEMBER_FALLBACK;
    }
  }
  return next;
}
