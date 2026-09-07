import assert from "node:assert/strict";
import { describe, it } from "node:test";

import { memberCookiePath } from "./member-cookie-path.ts";

describe("memberCookiePath", () => {
  it("defaults to Path=/ when the scoped flag is unset", () => {
    assert.equal(memberCookiePath({}), "/");
  });

  it("uses Path=/member only when SHOP_MEMBER_COOKIE_PATH_SCOPED=true", () => {
    assert.equal(memberCookiePath({ SHOP_MEMBER_COOKIE_PATH_SCOPED: "true" }), "/member");
  });

  it("stays Path=/ when the flag is not the string true", () => {
    assert.equal(memberCookiePath({ SHOP_MEMBER_COOKIE_PATH_SCOPED: "false" }), "/");
    assert.equal(memberCookiePath({ SHOP_MEMBER_COOKIE_PATH_SCOPED: "1" }), "/");
    assert.equal(memberCookiePath({ SHOP_MEMBER_COOKIE_PATH_SCOPED: "/member" }), "/");
  });
});
