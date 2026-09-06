import assert from "node:assert/strict";
import { describe, it } from "node:test";

import { cookieSecure } from "./cookie-secure.ts";

describe("cookieSecure", () => {
  it("is true when SHOP_COOKIE_SECURE=true (KeepAlive next dev on HTTPS)", () => {
    assert.equal(cookieSecure({ SHOP_COOKIE_SECURE: "true" }), true);
  });

  it("is true when NODE_ENV=production", () => {
    assert.equal(cookieSecure({ NODE_ENV: "production" }), true);
  });

  it("is true when both flags are set", () => {
    assert.equal(cookieSecure({ SHOP_COOKIE_SECURE: "true", NODE_ENV: "production" }), true);
  });

  it("is false for local http when unset", () => {
    assert.equal(cookieSecure({}), false);
  });

  it("is false when SHOP_COOKIE_SECURE is not the string true", () => {
    assert.equal(cookieSecure({ SHOP_COOKIE_SECURE: "false" }), false);
    assert.equal(cookieSecure({ SHOP_COOKIE_SECURE: "1" }), false);
  });
});
