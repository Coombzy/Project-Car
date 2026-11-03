import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

import { bookingStatusLabel } from "./booking-words.ts";

const webRoot = join(dirname(fileURLToPath(import.meta.url)), "..");
const cardPath = join(webRoot, "components/owner-booking-card.tsx");
const actionsPath = join(webRoot, "app/schedule/actions.ts");
const pagePath = join(webRoot, "app/schedule/page.tsx");

describe("owner finish visit", () => {
  it("drops the unused-time field and names a no-show", () => {
    const card = readFileSync(cardPath, "utf8");
    const actions = readFileSync(actionsPath, "utf8");
    const page = readFileSync(pagePath, "utf8");

    assert.equal(bookingStatusLabel("no_show"), "No-show");
    assert.match(card, /Finish visit/);
    assert.match(card, /bookingStatusLabel\(booking\.status\)/);
    assert.equal(card.includes("unused_tokens"), false);
    assert.equal(card.includes("Unused"), false);
    assert.equal(actions.includes("unused_tokens"), false);
    assert.match(page, /OwnerLaneGrid/);
    assert.match(page, /No-show/);
  });
});
