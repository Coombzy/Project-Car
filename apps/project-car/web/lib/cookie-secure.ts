/** Session cookie Secure flag.

Public HTTPS hosts (ops.projectcar.ca / app.projectcar.ca) need Secure even when
KeepAlive runs `next dev` and NODE_ENV is not production. Local
http://127.0.0.1:3000 should leave SHOP_COOKIE_SECURE unset or false.
*/
export function cookieSecure(env: NodeJS.ProcessEnv = process.env): boolean {
  return env.SHOP_COOKIE_SECURE === "true" || env.NODE_ENV === "production";
}
