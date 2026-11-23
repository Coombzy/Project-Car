/** Shared demo password. Server pages may show it only when showDemoLoginHints() is on. */
export const demoPassword = "changeme";

/** True only when SHOP_DEMO_LOGIN_HINTS=true. NODE_ENV is not a bypass. */
export function showDemoLoginHints(): boolean {
  return process.env["SHOP_DEMO_LOGIN_HINTS"] === "true";
}
