/** Hostname plus optional port. Rejects paths, credentials, and schemes. */
const HOST_RE = /^[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?(?::\d{1,5})?$/i;

function firstHop(value: string | null): string | null {
  if (!value) {
    return null;
  }
  const first = value.split(",")[0]?.trim();
  return first || null;
}

function safeHost(value: string | null): string | null {
  const host = firstHop(value);
  if (!host || !HOST_RE.test(host)) {
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
 * `X-Forwarded-Proto` when they look like a real host. Direct Doc demo stays
 * on `http://localhost:3000`.
 */
export function publicOrigin(headers: Pick<Headers, "get">, fallbackUrl: string): string {
  const host =
    safeHost(headers.get("x-forwarded-host")) ?? safeHost(headers.get("host"));
  if (!host) {
    return new URL(fallbackUrl).origin;
  }
  const proto = safeProto(headers.get("x-forwarded-proto")) ?? (isLocalHost(host) ? "http" : "https");
  return `${proto}://${host}`;
}

export function publicUrl(headers: Pick<Headers, "get">, fallbackUrl: string, path: string): URL {
  return new URL(path, publicOrigin(headers, fallbackUrl));
}
