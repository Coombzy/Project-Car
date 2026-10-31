const DEMO_OWNER_PASSWORD = "changeme";
const DEMO_MEMBER_PASSWORD = "changeme";

type DemoEnv = {
  NODE_ENV?: string;
  SHOP_DEMO_LOGIN_HINTS?: string;
};

/** Demo credentials render only outside production, or when the visual flag is on. */
export function showDemoLoginHints(env: DemoEnv = process.env): boolean {
  return env.NODE_ENV !== "production" || env.SHOP_DEMO_LOGIN_HINTS === "true";
}

export function demoOwnerEmail(): string {
  return "owner@projectcar.ca";
}

export function demoOwnerPassword(): string {
  return DEMO_OWNER_PASSWORD;
}

export function demoMemberEmail(): string {
  return "ada.reyes@example.com";
}

export function demoMemberPassword(): string {
  return DEMO_MEMBER_PASSWORD;
}
