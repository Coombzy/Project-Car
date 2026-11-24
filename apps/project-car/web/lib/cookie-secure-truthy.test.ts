import assert from "node:assert/strict";
import { it } from "node:test";
import { cookieSecure } from "./cookie-secure.ts";

it("treats trimmed case-insensitive truthy SHOP_COOKIE_SECURE values as true", () => {
  for (const v of ["1", "true", "TRUE", " yes "]) {
    assert.equal(cookieSecure({ SHOP_COOKIE_SECURE: v, NODE_ENV: "development" }), true);
  }
});

it("stays false for unset, empty and non-truthy SHOP_COOKIE_SECURE values", () => {
  for (const v of [undefined, "", "0", "false", "nope"]) {
    assert.equal(cookieSecure({ SHOP_COOKIE_SECURE: v, NODE_ENV: "development" }), false);
  }
});
