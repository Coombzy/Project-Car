/** Hostname plus optional port. Rejects paths, credentials, and schemes. */
const HOST_RE = /^[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?(?::\d{1,5})?$/i;

/**
 * Hosts that may drive middleware redirects / `publicOrigin`.
 * Hostname only (port stripped). `api.projectcar.ca` is intentionally absent —
 * it is the shop API, not a shop-web redirect host.
 */
const ALLOWED_PUBLIC_HOSTS = new Set([
  "localhost",
  "127.0.0.1",
  "ops.projectcar.ca",
  "app.projectcar.ca",
  "projectcar.ca",
  "www.projectcar.ca",
]);

/** Customer brochure hosts. Member UI may render here; Owner/ops UI may not. */
const CUSTOMER_SHOP_HOSTS = new Set(["projectcar.ca", "www.projectcar.ca"]);

/**
 * Fail-closed target when an Owner/ops path is requested on the customer host.
 * Absolute ops login — never a same-host `/login`, which would render management UI
 * on projectcar.ca. 307 (not 301): www→apex for `/member*` stays a later Zone hop.
 */
export const CUSTOMER_HOST_OPS_LOGIN = "https://ops.projectcar.ca/login";

function firstHop(value: string | null): string | null {
  if (!value) {
    return null;
  }
  const first = value.split(",")[0]?.trim();
  return first || null;
}

function hostnameOf(host: string): string {
  return host.split(":")[0]?.toLowerCase() ?? "";
}

function safeHost(value: string | null): string | null {
  const host = firstHop(value);
  if (!host || !HOST_RE.test(host)) {
    return null;
  }
  return host;
}

function allowedHost(value: string | null): string | null {
  const host = safeHost(value);
  if (!host || !ALLOWED_PUBLIC_HOSTS.has(hostnameOf(host))) {
    return null;
  }
  return host;
}

function safeProto(value: string | null): "http" | "https" | null {
  const proto = firstHop(value)?.toLowerCase() ?? null;
  if (proto === "http" || proto === "https") {
    return proto;
  }
  return null;
}

function isLocalHost(host: string): boolean {
  const name = host.split(":")[0]?.toLowerCase() ?? "";
  return name === "localhost" || name === "127.0.0.1";
}

/**
 * Origin for middleware redirects.
 *
 * Next 15 rebuilds `request.url` from the listen address (`localhost:3000`)
 * whenever hostname+port are set, so `experimental.trustHostHeader` does not
 * fix Cloudflare Tunnel → Doc. Honor `X-Forwarded-Host` / `Host` plus
 * `X-Forwarded-Proto` when they look like a real host **and** the host is on
 * the explicit allowlist. Junk or unknown `X-Forwarded-Host` / `Host` cannot
 * mint a login redirect to a random origin. Direct Doc demo stays on
 * `http://localhost:3000`.
 */
export function publicOrigin(headers: Pick<Headers, "get">, fallbackUrl: string): string {
  const host =
    allowedHost(headers.get("x-forwarded-host")) ?? allowedHost(headers.get("host"));
  if (!host) {
    return new URL(fallbackUrl).origin;
  }
  const proto = safeProto(headers.get("x-forwarded-proto")) ?? (isLocalHost(host) ? "http" : "https");
  return `${proto}://${host}`;
}

export function publicUrl(headers: Pick<Headers, "get">, fallbackUrl: string, path: string): URL {
  return new URL(path, publicOrigin(headers, fallbackUrl));
}

/** Allowlisted hostname from `X-Forwarded-Host`, else `Host`. Null if neither is allowlisted. */
export function allowlistedHostname(headers: Pick<Headers, "get">): string | null {
  const host = allowedHost(headers.get("x-forwarded-host")) ?? allowedHost(headers.get("host"));
  if (!host) {
    return null;
  }
  return hostnameOf(host);
}

/** True only for projectcar.ca and www.projectcar.ca. ops, app, and localhost are not. */
export function isCustomerShopHost(headers: Pick<Headers, "get">): boolean {
  const name = allowlistedHostname(headers);
  return name !== null && CUSTOMER_SHOP_HOSTS.has(name);
}

/**
 * On the customer host, shop-web may render Member routes only.
 * `/members` (Owner list) and `/membership` are not Member UI.
 * `_next/*` and favicon are allowed so a matcher change cannot serve ops HTML for assets.
 */
export function customerHostAllowsPath(pathname: string): boolean {
  if (pathname === "/member" || pathname.startsWith("/member/")) {
    return true;
  }
  if (pathname === "/favicon.ico" || pathname.startsWith("/_next/")) {
    return true;
  }
  return false;
}
