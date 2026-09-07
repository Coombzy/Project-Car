/** Member session cookie Path.

Default `Path=/` (whole shop-web origin — current ops/app/localhost behavior).

Set `SHOP_MEMBER_COOKIE_PATH_SCOPED=true` to use `Path=/member` so a future
share-host cutover would not send `pc_member_session` to brochure pages.
Login, logout, and `delete` must use this same helper. Production Doc env
stays unset / OFF until Ben GO — do not flip it in this prep.
*/
export function memberCookiePath(env: NodeJS.ProcessEnv = process.env): "/" | "/member" {
  return env.SHOP_MEMBER_COOKIE_PATH_SCOPED === "true" ? "/member" : "/";
}
