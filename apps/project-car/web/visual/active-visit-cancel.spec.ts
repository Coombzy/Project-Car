import { expect, test } from "@playwright/test";

import { MEMBER_SESSION_COOKIE, SESSION_COOKIE } from "../lib/config";

const API = "http://127.0.0.1:8000";
const WEB = "http://127.0.0.1:3000";

type HoistRow = {
  id: string;
  name: string;
  is_shop: boolean;
};

function cookieValue(headers: string[], name: string): string {
  for (const header of headers) {
    const pair = header.split(";", 1)[0] ?? "";
    const eq = pair.indexOf("=");
    if (eq === -1) {
      continue;
    }
    if (pair.slice(0, eq).trim() !== name) {
      continue;
    }
    return decodeURIComponent(pair.slice(eq + 1).trim());
  }
  throw new Error(`login did not set ${name}`);
}

async function login(path: string, email: string, password: string, cookieName: string): Promise<string> {
  const response = await fetch(`${API}${path}`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });
  if (!response.ok) {
    throw new Error(`${path} login failed: ${response.status} ${await response.text()}`);
  }
  return cookieValue(response.headers.getSetCookie(), cookieName);
}

async function apiGet<T>(path: string, cookieName: string, token: string): Promise<T> {
  const response = await fetch(`${API}${path}`, {
    headers: {
      Accept: "application/json",
      Cookie: `${cookieName}=${encodeURIComponent(token)}`,
    },
  });
  if (!response.ok) {
    throw new Error(`${path} ${response.status} ${await response.text()}`);
  }
  return (await response.json()) as T;
}

test("test_seeded_active_visit_hides_cancel", async ({ page }) => {
  const owner = await login("/auth/login", "owner@projectcar.ca", "changeme", SESSION_COOKIE);
  const riley = await login("/auth/member/login", "riley.park@example.com", "changeme", MEMBER_SESSION_COOKIE);
  const hoists = await apiGet<HoistRow[]>("/hoists", SESSION_COOKIE, owner);
  const bay2 = hoists.find((row) => row.name === "Bay 2" && row.is_shop === false);
  const bay1 = hoists.find((row) => row.name === "Bay 1" && row.is_shop === false);
  if (!bay2 || !bay1) {
    throw new Error("seed is missing Bay 1 or Bay 2");
  }

  async function openWeek(path: string, cookieName: string, token: string): Promise<void> {
    await page.context().clearCookies();
    await page.context().addCookies([
      { name: cookieName, value: token, url: WEB, httpOnly: true, sameSite: "Lax" },
    ]);
    const response = await page.goto(path, { waitUntil: "load" });
    expect(response, path).not.toBeNull();
    expect(response?.status(), path).toBeLessThan(400);
    if (page.url().includes("/login")) {
      throw new Error(`expected an authenticated page, landed on ${page.url()}`);
    }
    await expect(page.getByText("Cannot reach shop API")).toHaveCount(0);
  }

  function chip(hoistId: string, name: string, start: RegExp, end: RegExp) {
    return page
      .locator(`#hoist-${hoistId} .hour-booking`)
      .filter({ hasText: name })
      .filter({ hasText: start })
      .filter({ hasText: end });
  }

  await openWeek("/schedule?view=week", SESSION_COOKIE, owner);
  const active = chip(bay2.id, "Riley Park", /9:00\s*a\.m\./, /11:00\s*a\.m\./);
  await expect(active).toHaveCount(1);
  await expect(active.locator("[data-booking-status=active]")).toHaveCount(1);
  await expect(active.locator("button", { hasText: "Cancel" })).toHaveCount(0);
  await expect(active.locator("button", { hasText: "Complete" })).toHaveCount(1);
  const ada = chip(bay1.id, "Ada Reyes", /2:00\s*p\.m\./, /4:00\s*p\.m\./);
  await expect(ada).toHaveCount(1);
  await expect(ada.locator("button", { hasText: "Cancel" })).toHaveCount(1);
  await expect(ada.locator("button", { hasText: "Complete" })).toHaveCount(0);

  await openWeek("/member/schedule?view=week", MEMBER_SESSION_COOKIE, riley);
  const ownActive = chip(bay2.id, "You", /9:00\s*a\.m\./, /11:00\s*a\.m\./);
  await expect(ownActive).toHaveCount(1);
  await expect(ownActive.locator("[data-booking-status=active]")).toHaveCount(1);
  await expect(ownActive.locator("button", { hasText: "Cancel" })).toHaveCount(0);
  await expect(ownActive.locator("button", { hasText: "Complete" })).toHaveCount(0);
  const ownConfirmed = page
    .locator(`#hoist-${bay2.id} .hour-booking`)
    .filter({ hasText: "You" })
    .filter({ has: page.locator(".pill-confirmed") });
  await expect(ownConfirmed).toHaveCount(1);
  await expect(ownConfirmed.locator("button", { hasText: "Cancel" })).toHaveCount(1);
  await expect(ownConfirmed.locator("button", { hasText: "Complete" })).toHaveCount(0);
});
