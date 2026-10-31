const SHOP_CLIENT_IP = "X-Shop-Client-IP";
const SHOP_PROXY_SECRET_HEADER = "X-Shop-Proxy-Secret";

type HeaderList = { get(name: string): string | null };
type ProxyEnv = { SHOP_PROXY_SECRET?: string };

/** Forward Cloudflare's client IP only when the shop shares a proxy secret. */
export function loginForwardHeaders(
  headerList: HeaderList,
  env: ProxyEnv = process.env,
): Record<string, string> {
  const secret = (env.SHOP_PROXY_SECRET ?? "").trim();
  const ip = (headerList.get("cf-connecting-ip") ?? "").trim();
  if (!secret || !ip) {
    return {};
  }
  return {
    [SHOP_CLIENT_IP]: ip,
    [SHOP_PROXY_SECRET_HEADER]: secret,
  };
}
