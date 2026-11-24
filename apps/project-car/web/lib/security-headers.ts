export type SecurityHeader = {
  key: string;
  value: string;
};

/** Headers on every shop-web response, including redirects and the web manifest. */
export const SECURITY_HEADERS: readonly SecurityHeader[] = [
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  { key: "X-Frame-Options", value: "DENY" },
  { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=()" },
  { key: "Strict-Transport-Security", value: "max-age=31536000; includeSubDomains" },
  // Starter CSP only. script-src with Next.js nonces is a later row.
  {
    key: "Content-Security-Policy",
    value: "frame-ancestors 'none'; object-src 'none'; base-uri 'self'",
  },
];

type HeaderWriter = {
  headers: { set(name: string, value: string): void };
};

export function applySecurityHeaders<T extends HeaderWriter>(response: T): T {
  for (const header of SECURITY_HEADERS) {
    response.headers.set(header.key, header.value);
  }
  return response;
}
