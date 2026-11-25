import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { describe, it } from "node:test";

import { cookieLooksPlausible, sessionExpiredTarget } from "./session-expired.ts";

const TOKEN =
  "eyJyb2xlIjoib3duZXIiLCJlbWFpbCI6Im93bmVyQHByb2plY3RjYXIuY2EifQ.awY3WQ.PipaHWSf6mhE5_7H8JyoVDXhfbY";
const read = (path: string) => readFileSync(new URL(path, import.meta.url), "utf8");
describe("sessionExpiredTarget", () => {
  it("returns the logout handlers", () => {
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
    for (const value of ["", " ", " \t\n", "\t", "\n", "\u00a0", "a b", `${TOKEN} `, "a\nb", "a\u0000b", "a\u007fb"]) {
      assert.equal(cookieLooksPlausible(value), false, JSON.stringify(value));
    }
  });
});

describe("expired session leaves the Server Component", () => {
  it("page.ts redirects and does not import the cookie writers", () => {
    const page = read("./page.ts");
    assert.match(page, /export async function handlePageError/);
    assert.match(page, /export async function handleMemberPageError/);
    assert.match(page, /redirect\(sessionExpiredTarget\("owner"\)\)/);
    assert.match(page, /redirect\(sessionExpiredTarget\("member"\)\)/);
    assert.equal(page.match(/return shopErrorMessage\(error\)/g)?.length, 2);
    assert.doesNotMatch(page, /clearSessionCookie/);
    assert.doesNotMatch(page, /clearMemberSessionCookie/);
    assert.doesNotMatch(page, /from ["']\.\/session["']/);
  });

  it("a bad cookie does not redirect the other audience", () => {
    const source = read("../middleware.ts");
    const memberAt = source.indexOf("if (isMemberArea && path !== memberExpired");
    const ownerAt = source.indexOf("if (!isMemberArea && !isSignup");
    const memberGate = source.slice(memberAt, ownerAt);
    const ownerGate = source.slice(ownerAt, source.indexOf("if (isMemberLogin)"));
    assert.doesNotMatch(source, /session-expired/);
    assert.match(source, /function cookieLooksPlausible\(/);
    assert.match(memberGate, /cookieLooksPlausible\(memberSession\)/);
    assert.doesNotMatch(memberGate, /ownerExpired/);
    assert.match(ownerGate, /cookieLooksPlausible\(ownerSession\)/);
    assert.doesNotMatch(ownerGate, /memberExpired/);
  });

  it("handlers clear the matching cookie and do not catch redirect", () => {
    const owner = read("../app/logout/expired/route.ts");
    const member = read("../app/member/logout/expired/route.ts");
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
