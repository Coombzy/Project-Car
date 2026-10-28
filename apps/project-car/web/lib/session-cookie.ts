// Lockstep with SESSION_COOKIE / MEMBER_SESSION_COOKIE in ./config.
// No import: node --test cannot resolve an extensionless relative specifier,
// and a ".ts" specifier fails tsc without allowImportingTsExtensions.
const SESSION_COOKIE = "pc_owner_session";
const MEMBER_SESSION_COOKIE = "pc_member_session";

export function extractNamedCookie(setCookieHeaders: string[], cookieName: string): string | null {
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
