/** Stand-in for the tunnel client-IP header. Backlog R106. */
export const EDGE_CLIENT_IP_HEADER = "CF-Connecting-IP";

const SHOP_CLIENT_IP_HEADER = "X-Shop-Client-IP";
const SHOP_PROXY_SECRET_HEADER = "X-Shop-Proxy-Secret";

type HeaderSource = {
  headers: { get(name: string): string | null };
};

/** Headers the API uses to rate-limit the browser instead of the Next.js server. */
export function loginForwardHeaders(request: HeaderSource, secret: string): Record<string, string> {
  const forwarded: Record<string, string> = {};
  const clientIp = request.headers.get(EDGE_CLIENT_IP_HEADER)?.trim() ?? "";
  if (clientIp !== "") {
    forwarded[SHOP_CLIENT_IP_HEADER] = clientIp;
  }
  const proxySecret = secret.trim();
  if (proxySecret !== "") {
    forwarded[SHOP_PROXY_SECRET_HEADER] = proxySecret;
  }
  return forwarded;
}
