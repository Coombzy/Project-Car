import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

const card = readFileSync(
  join(dirname(fileURLToPath(import.meta.url)), "../components/member-booking-card.tsx"),
  "utf8",
);

describe("member booking card copy", () => {
  it("names Mountain Time and requires a Yes, cancel checkbox", () => {
    assert.equal(card.includes("· Mountain Time"), true);
    assert.match(card, /<input type="checkbox" name="confirm" value="yes" required \/>/);
    assert.equal(card.includes("Yes, cancel"), true);
    assert.equal(card.includes("{cancel.confirmText}"), true);
    assert.equal(card.includes("{cancel.note}"), true);
    assert.equal(card.includes('from "../lib/booking-calendar"'), true);
    assert.equal(card.includes("memberCancelOffer"), true);
    assert.equal(card.includes("offersCancel"), false);
  });
});
