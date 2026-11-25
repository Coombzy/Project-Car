import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { describe, it } from "node:test";

import { cookieLooksPlausible, sessionExpiredTarget } from "./session-expired.ts";

// itsdangerous URLSafeTimedSerializer shape: payload.timestamp.signature.
const TOKEN =
  "eyJyb2xlIjoib3duZXIiLCJlbWFpbCI6Im93bmVyQHByb2plY3RjYXIuY2EifQ.awY3WQ.PipaHWSf6mhE5_7H8JyoVDXhfbY";

function source(relativePath: string): string {
  return readFileSync(new URL(relativePath, import.meta.url), "utf8");
}

describe("sessionExpiredTarget", () => {
  it("returns the owner and member logout handlers", () => {
    assert.equal(sessionExpiredTarget("owner"), "/logout/expired");
    assert.equal(sessionExpiredTarget("member"), "/member/logout/expired");
  });
});

describe("cookieLooksPlausible", () => {
  it("accepts a normal URL-safe timed session token", () => {
    assert.equal(cookieLooksPlausible(TOKEN), true);
    assert.equal(cookieLooksPlausible("Ab3._-"), true);
  });

  it("rejects empty, whitespace-only, spaces, and ASCII controls", () => {
    const rejected = [
      "",
      " ",
      " \t\n",
      "\t",
      "\n",
      "\r",
      "\u00a0",
      "a b",
      `${TOKEN} `,
      ` ${TOKEN}`,
      "a\nb",
      "a\u0000b",
      "a\u007fb",
      "\u0001",
    ];
    for (const value of rejected) {
      assert.equal(cookieLooksPlausible(value), false, JSON.stringify(value));
    }
  });
});

describe("expired session leaves the Server Component", () => {
  it("page.ts redirects to the handlers and does not import the cookie writers", () => {
    const page = source("./page.ts");
    assert.match(page, /export async function handlePageError/);
    assert.match(page, /export async function handleMemberPageError/);
    assert.match(page, /redirect\(sessionExpiredTarget\("owner"\)\)/);
    assert.match(page, /redirect\(sessionExpiredTarget\("member"\)\)/);
    assert.equal(page.match(/return shopErrorMessage\(error\)/g)?.length, 2);
    assert.doesNotMatch(page, /clearSessionCookie/);
    assert.doesNotMatch(page, /clearMemberSessionCookie/);
    assert.doesNotMatch(page, /from ["']\.\/session["']/);
  });

  it("middleware.ts uses cookieLooksPlausible", () => {
    const middleware = source("../middleware.ts");
    assert.match(middleware, /cookieLooksPlausible\(/);
    assert.match(middleware, /sessionExpiredTarget\(/);
  });

  it("route handlers clear the matching cookie and do not catch redirect", () => {
    const owner = source("../app/logout/expired/route.ts");
    const member = source("../app/member/logout/expired/route.ts");
    assert.match(owner, /clearSessionCookie\(/);
    assert.doesNotMatch(owner, /clearMemberSessionCookie/);
    assert.match(owner, /redirect\("\/login\?reason=session"\)/);
    assert.doesNotMatch(owner, /\btry\b/);
    assert.match(member, /clearMemberSessionCookie\(/);
    assert.doesNotMatch(member, /clearSessionCookie\(/);
    assert.match(member, /redirect\("\/member\/login\?reason=session"\)/);
    assert.doesNotMatch(member, /\btry\b/);
  });
});
