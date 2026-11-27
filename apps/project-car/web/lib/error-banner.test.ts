import assert from "node:assert/strict";
import { test } from "node:test";

import { bannerMessage } from "./error-banner.ts";

test("chat_update_failed maps to the fixed chat message", () => {
  assert.equal(bannerMessage("chat_update_failed"), "Chat update failed.");
});

test("missing sku code and the current sentence map to the same banner", () => {
  assert.equal(bannerMessage("missing_sku"), "Enter a part number.");
  assert.equal(bannerMessage("Enter a part number."), "Enter a part number.");
});

test("parts failure code and the current sentence map to the same banner", () => {
  assert.equal(bannerMessage("parts_request_failed"), "Parts request failed.");
  assert.equal(bannerMessage("Parts request failed."), "Parts request failed.");
});

test("unknown query text renders no banner", () => {
  assert.equal(bannerMessage("anything"), null);
  assert.equal(bannerMessage("Click here to reset your password"), null);
  assert.equal(bannerMessage("toString"), null);
  assert.equal(bannerMessage("constructor"), null);
  assert.equal(bannerMessage("__proto__"), null);
  assert.equal(bannerMessage(undefined), null);
  assert.equal(bannerMessage(null), null);
});
