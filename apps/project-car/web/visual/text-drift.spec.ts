import { expect, test, type Page } from "@playwright/test";

import { SESSION_COOKIE } from "../lib/config";
import { tokensLabel } from "../lib/time";
import { OFFICIAL_1440_BODY } from "../lib/visual-text-drift";

const API = "http://127.0.0.1:8000";
const WEB = "http://127.0.0.1:3000";

function cookieValue(headers: string[], name: string): string {
  for (const header of headers) {
    const pair = (header.split(";", 1)[0] ?? "").trim();
    const eq = pair.indexOf("=");
    if (eq > 0 && pair.slice(0, eq) === name) return decodeURIComponent(pair.slice(eq + 1));
  }
  throw new Error(`login did not set ${name}`);
}

async function ownerSession(): Promise<{ token: string; adaId: string }> {
  const login = await fetch(`${API}/auth/login`, {
    method: "POST",
    headers: { Accept: "application/json", "Content-Type": "application/json" },
    body: JSON.stringify({ email: "owner@projectcar.ca", password: "changeme" }),
  });
  if (!login.ok) throw new Error(`login failed: ${login.status} ${await login.text()}`);
  const token = cookieValue(login.headers.getSetCookie(), SESSION_COOKIE);
  const listed = await fetch(`${API}/members`, {
    headers: { Accept: "application/json", Cookie: `${SESSION_COOKIE}=${encodeURIComponent(token)}` },
  });
  if (!listed.ok) throw new Error(`/members ${listed.status} ${await listed.text()}`);
  const ada = ((await listed.json()) as { id: string; email: string }[]).find((row) => row.email === "ada.reyes@example.com");
  if (!ada) throw new Error("seed is missing Ada Reyes");
  return { token, adaId: ada.id };
}

async function open(page: Page, path: string): Promise<void> {
  const response = await page.goto(path, { waitUntil: "load" });
  expect(response, path).not.toBeNull();
  expect(response?.status(), path).toBeLessThan(400);
  expect(page.url(), path).not.toContain("/login");
}

test("1440 owner body matches the frozen clock", async ({ page, context }, testInfo) => {
  test.skip(testInfo.project.name !== "1440", "1440 only");
  const { token, adaId } = await ownerSession();
  await context.addCookies([{ name: SESSION_COOKIE, value: token, url: WEB, httpOnly: true, sameSite: "Lax" }]);
  const ada = tokensLabel(OFFICIAL_1440_BODY.adaTokens);
  await open(page, "/");
  await expect(page.getByText(OFFICIAL_1440_BODY.tokensAtRisk).first()).toBeVisible();
  for (const path of ["/members", `/members/${adaId}`]) {
    await open(page, path);
    await expect(page.getByText(ada).first()).toBeVisible();
  }
  await open(page, "/tiers");
  for (const band of OFFICIAL_1440_BODY.bands) await expect(page.getByText(band).first()).toBeVisible();
});
