/**
 * Copy-event ICS fetches stay on this origin.
 * Accept /todos/{id}/ics and /member/todos/{id}/ics, including the same
 * path as an absolute URL on `origin`. Return that root-relative path.
 */

const ICS_PATH = /^\/(?:member\/)?todos\/[A-Za-z0-9-]+\/ics$/;
const UNSAFE = /[\u0000-\u001F\u007F\\]/;

function httpOrigin(value: string): string | null {
  if (value !== value.trim() || UNSAFE.test(value)) {
    return null;
  }
  try {
    const url = new URL(value);
    if ((url.protocol !== "http:" && url.protocol !== "https:") || url.username || url.password) {
      return null;
    }
    return url.origin;
  } catch {
    return null;
  }
}

export function safeIcsHref(href: string, origin: string): string | null {
  const base = httpOrigin(origin);
  if (
    !base ||
    href !== href.trim() ||
    UNSAFE.test(href) ||
    href.includes("..") ||
    href.includes("/./") ||
    href.includes("%")
  ) {
    return null;
  }
  let url: URL;
  try {
    url = new URL(href, base);
  } catch {
    return null;
  }
  const rootRelative = href.startsWith("/") && !href.startsWith("//");
  if (
    url.origin !== base ||
    url.username ||
    url.password ||
    url.search ||
    url.hash ||
    !ICS_PATH.test(url.pathname) ||
    (!rootRelative && httpOrigin(href) !== base)
  ) {
    return null;
  }
  return url.pathname;
}
