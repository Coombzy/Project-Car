import assert from "node:assert/strict";
import { existsSync, readdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

import { ShopApiError } from "./config.ts";
import { isMemberSessionError, isOwnerSessionError, shopErrorMessage } from "./shop-error.ts";

const webRoot = join(dirname(fileURLToPath(import.meta.url)), "..");

const FALLBACK = "Something went wrong talking to the shop API.";
const api = (status: number) => new ShopApiError(status, "code", `message ${status}`);
// Same keys as a ShopApiError, but not one: must never leak its message or log anyone out.
const lookalike = { status: 401, code: "ECONNREFUSED", message: "internal db host 10.0.0.5" };
const notApi: unknown[] = [new Error("boom"), "just a string", lookalike];

describe("shopErrorMessage", () => {
  it("returns the ShopApiError message, even with a custom fallback", () => {
    assert.equal(shopErrorMessage(api(404)), "message 404");
    assert.equal(shopErrorMessage(api(500), "custom"), "message 500");
  });

  it("returns the fallback for anything else", () => {
    for (const error of notApi) {
      assert.equal(shopErrorMessage(error), FALLBACK);
      assert.equal(shopErrorMessage(error, "custom"), "custom");
    }
  });
});

describe("session errors", () => {
  const cases: [number, boolean, boolean][] = [
    [401, true, true],
    [403, false, true],
    [404, false, false],
    [500, false, false],
  ];
  for (const [status, owner, member] of cases) {
    it(`ShopApiError ${status}: owner=${owner} member=${member}`, () => {
      assert.equal(isOwnerSessionError(api(status)), owner);
      assert.equal(isMemberSessionError(api(status)), member);
    });
  }

  it("anything that is not a ShopApiError is never a session error", () => {
    for (const error of notApi) {
      assert.equal(isOwnerSessionError(error), false);
      assert.equal(isMemberSessionError(error), false);
    }
  });
});

describe("page.ts session redirect stays on the login URL", () => {
  const pageSource = readFileSync(join(webRoot, "lib/page.ts"), "utf8");

  it("re-exports the helpers and still clears the cookie on the way to login", () => {
    assert.match(pageSource, /export\s*\{[^}]*\bshopErrorMessage\b/);
    assert.match(pageSource, /export\s*\{[^}]*\bisOwnerSessionError\b/);
    assert.match(pageSource, /export\s*\{[^}]*\bisMemberSessionError\b/);
    assert.match(pageSource, /clearSessionCookie\(/);
    assert.match(pageSource, /clearMemberSessionCookie\(/);
    assert.match(pageSource, /redirect\("\/login\?reason=session"\)/);
    assert.match(pageSource, /redirect\("\/member\/login\?reason=session"\)/);
    assert.equal(pageSource.includes("/session/expired"), false);
    assert.equal(existsSync(join(webRoot, "app/session/expired/route.ts")), false);
    assert.equal(existsSync(join(webRoot, "app/member/session/expired/route.ts")), false);
    assert.equal(existsSync(join(webRoot, "lib/page-error.test.ts")), false);
    for (const width of ["390", "768", "1440"]) {
      const names = readdirSync(join(webRoot, "visual/screenshots", width));
      assert.equal(
        names.some((name) => name.startsWith("r79-")),
        false,
        `${width} still has an r79 proof shot`,
      );
    }
  });
});
