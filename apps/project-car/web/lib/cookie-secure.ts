/** Session cookie Secure flag.

Public HTTPS hosts (ops.projectcar.ca / app.projectcar.ca) need Secure even when
KeepAlive runs `next dev` and NODE_ENV is not production. Local
http://127.0.0.1:3000 should leave SHOP_COOKIE_SECURE unset or false.
*/
const TRUTHY_FLAGS = new Set(["1", "true", "yes"]);

export function cookieSecure(env: NodeJS.ProcessEnv = process.env): boolean {
  const flag = env.SHOP_COOKIE_SECURE?.trim().toLowerCase();
  return (flag !== undefined && TRUTHY_FLAGS.has(flag)) || env.NODE_ENV === "production";
}
