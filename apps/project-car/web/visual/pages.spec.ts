import { expect, test, type Page } from "@playwright/test";

import { MEMBER_SESSION_COOKIE, SESSION_COOKIE } from "../lib/config";

const API = "http://127.0.0.1:8000";
const WEB = "http://127.0.0.1:3000";
const MAX_LAYOUT_SHIFT = 0.1;
const SETTLE_MS = 800;

type Auth = "public" | "owner" | "member";

type Shot = {
  name: string;
  path: string;
};

type MemberRow = {
  id: string;
  email: string;
};

type RoomRow = {
  id: string;
  title: string;
};

const PUBLIC_PAGES: Shot[] = [
  { name: "login", path: "/login" },
  { name: "member-login", path: "/member/login" },
];

const OWNER_PAGES: Shot[] = [
  { name: "home", path: "/" },
  { name: "cameras", path: "/cameras" },
  { name: "chat", path: "/chat" },
  { name: "fill", path: "/fill" },
  { name: "hoists", path: "/hoists" },
  { name: "jobs", path: "/jobs" },
  { name: "members", path: "/members" },
  { name: "parts", path: "/parts" },
  { name: "payments", path: "/payments" },
  { name: "schedule", path: "/schedule" },
  { name: "tiers", path: "/tiers" },
  { name: "tools", path: "/tools" },
  { name: "waitlist", path: "/waitlist" },
];

const MEMBER_PAGES: Shot[] = [
  { name: "member-home", path: "/member" },
  { name: "member-cameras", path: "/member/cameras" },
  { name: "member-chat", path: "/member/chat" },
  { name: "member-jobs", path: "/member/jobs" },
  { name: "member-parts", path: "/member/parts" },
  { name: "member-schedule", path: "/member/schedule" },
];

const ADA_EMAIL = "ada.reyes@example.com";
const ADA_ROOM = "Ada — turbo mock-up";

let ownerToken = "";
let memberToken = "";
let adaMemberId = "";
let ownerRoomId = "";
let memberRoomId = "";

function assertAuth(auth: Auth, url: string): void {
  switch (auth) {
    case "public":
      return;
    case "owner":
    case "member":
      if (url.includes("/login")) {
        throw new Error(`expected an authenticated ${auth} page, landed on ${url}`);
      }
      return;
    default: {
      const neverAuth: never = auth;
      throw new Error(`unknown auth ${String(neverAuth)}`);
    }
  }
}

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

async function shoot(page: Page, path: string, name: string, auth: Auth): Promise<void> {
  const response = await page.goto(path, { waitUntil: "load" });
  expect(response, path).not.toBeNull();
  expect(response?.status(), path).toBeLessThan(400);
  assertAuth(auth, page.url());
  await page.evaluate(() => document.fonts.ready);
  await page.waitForLoadState("networkidle");
  await page.waitForTimeout(SETTLE_MS);
  await expect(page.getByText("Cannot reach shop API")).toHaveCount(0);
  const cls = await page.evaluate(() => {
    const measured = (window as Window & { __cls?: number }).__cls;
    return typeof measured === "number" ? measured : 0;
  });
  expect(cls, `${path} layout shift ${cls}`).toBeLessThanOrEqual(MAX_LAYOUT_SHIFT);
  await expect(page).toHaveScreenshot(`${name}.png`);
}

test.beforeAll(async () => {
  ownerToken = await login("/auth/login", "owner@projectcar.ca", "changeme", SESSION_COOKIE);
  memberToken = await login("/auth/member/login", ADA_EMAIL, "changeme", MEMBER_SESSION_COOKIE);
  const members = await apiGet<MemberRow[]>("/members", SESSION_COOKIE, ownerToken);
  const ada = members.find((row) => row.email === ADA_EMAIL);
  if (!ada) {
    throw new Error("seed is missing Ada Reyes");
  }
  adaMemberId = ada.id;
  const rooms = await apiGet<RoomRow[]>("/chat/rooms", SESSION_COOKIE, ownerToken);
  const room = rooms.find((row) => row.title === ADA_ROOM);
  if (!room) {
    throw new Error("seed is missing the Ada turbo room");
  }
  ownerRoomId = room.id;
  const memberRooms = await apiGet<RoomRow[]>("/member/chat/rooms", MEMBER_SESSION_COOKIE, memberToken);
  const memberRoom = memberRooms.find((row) => row.id === room.id);
  if (!memberRoom) {
    throw new Error("Ada cannot see the turbo room");
  }
  memberRoomId = memberRoom.id;
});

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => {
    const scope = window as Window & { __cls?: number };
    scope.__cls = 0;
    const observer = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        const shift = entry as PerformanceEntry & { value?: number; hadRecentInput?: boolean };
        if (shift.hadRecentInput || typeof shift.value !== "number") {
          continue;
        }
        scope.__cls = (scope.__cls ?? 0) + shift.value;
      }
    });
    observer.observe({ type: "layout-shift", buffered: true });
  });
});

test.describe("public pages", () => {
  for (const shot of PUBLIC_PAGES) {
    test(shot.name, async ({ page }) => {
      await shoot(page, shot.path, shot.name, "public");
    });
  }
});

test.describe("owner pages", () => {
  test.beforeEach(async ({ context }) => {
    await context.addCookies([
      { name: SESSION_COOKIE, value: ownerToken, url: WEB, httpOnly: true, sameSite: "Lax" },
    ]);
  });

  for (const shot of OWNER_PAGES) {
    test(shot.name, async ({ page }) => {
      await shoot(page, shot.path, shot.name, "owner");
    });
  }

  test("member-detail", async ({ page }) => {
    await shoot(page, `/members/${adaMemberId}`, "member-detail", "owner");
  });

  test("chat-room", async ({ page }) => {
    await shoot(page, `/chat/${ownerRoomId}`, "chat-room", "owner");
  });
});

test.describe("member pages", () => {
  test.beforeEach(async ({ context }) => {
    await context.addCookies([
      { name: MEMBER_SESSION_COOKIE, value: memberToken, url: WEB, httpOnly: true, sameSite: "Lax" },
    ]);
  });

  for (const shot of MEMBER_PAGES) {
    test(shot.name, async ({ page }) => {
      await shoot(page, shot.path, shot.name, "member");
    });
  }

  test("member-chat-room", async ({ page }) => {
    await shoot(page, `/member/chat/${memberRoomId}`, "member-chat-room", "member");
  });
});
