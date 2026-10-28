import assert from "node:assert/strict";
import { describe, it } from "node:test";

import { MEMBER_SESSION_COOKIE, SESSION_COOKIE } from "./config.ts";
import { extractMemberSessionValue, extractSessionValue } from "./session-cookie.ts";

describe("extractSessionValue", () => {
  it("finds the owner cookie among several Set-Cookie headers", () => {
    const headers = [
      "theme=dark; Path=/",
      `${MEMBER_SESSION_COOKIE}=member-token; HttpOnly; Path=/`,
      `${SESSION_COOKIE}=owner-token; HttpOnly; Secure; Path=/`,
    ];
    assert.equal(extractSessionValue(headers), "owner-token");
  });

  it("decodes a percent-encoded value", () => {
    assert.equal(extractSessionValue([`${SESSION_COOKIE}=a%2Fb%20c; Path=/`]), "a/b c");
  });

  it("returns a bad escape like %E0%A4%A raw", () => {
    assert.equal(extractSessionValue([`${SESSION_COOKIE}=%E0%A4%A; HttpOnly`]), "%E0%A4%A");
  });

  it("skips a header with no equals and still reads a later owner cookie", () => {
    const headers = ["HttpOnly", SESSION_COOKIE, `${SESSION_COOKIE}=owner-token; Path=/`];
    assert.equal(extractSessionValue(headers), "owner-token");
  });

  it("returns null for an empty array", () => {
    assert.equal(extractSessionValue([]), null);
  });

  it("returns null when no header matches the owner cookie", () => {
    assert.equal(
      extractSessionValue([`${MEMBER_SESSION_COOKIE}=member-token; Path=/`, "other=1"]),
      null,
    );
  });

  it("ignores attributes after the first semicolon", () => {
    assert.equal(
      extractSessionValue([`${SESSION_COOKIE}=owner-token; HttpOnly; Path=/member; Secure`]),
      "owner-token",
    );
  });
});

describe("extractMemberSessionValue", () => {
  it("returns the member cookie and not the owner cookie", () => {
    const headers = [
      `${SESSION_COOKIE}=owner-token; HttpOnly; Secure; Path=/`,
      `${MEMBER_SESSION_COOKIE}=member-token; HttpOnly; Path=/`,
    ];
    assert.equal(extractMemberSessionValue(headers), "member-token");
    assert.equal(extractSessionValue(headers), "owner-token");
  });

  it("returns null for an empty array and when only the owner cookie is present", () => {
    assert.equal(extractMemberSessionValue([]), null);
    assert.equal(extractMemberSessionValue([`${SESSION_COOKIE}=owner-token; Path=/`]), null);
  });
});
