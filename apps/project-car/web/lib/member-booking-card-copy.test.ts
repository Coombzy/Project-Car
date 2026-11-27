import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

import { memberCancelOffer } from "./booking-calendar.ts";

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
    assert.match(card, /slot\.hoist_name/);
  });

  it("shownCancel passes confirm copy and labels the button Cancel", async () => {
    const offer = memberCancelOffer(
      { status: "confirmed", startAt: "2026-11-07T16:00:00", reservedTokens: "80" },
      new Date("2026-11-05T22:00:00.000Z"),
    );
    assert.equal(offer.visible, true);
    assert.equal(offer.confirmText, "Cancel this visit? You get 80 tokens back.");
    assert.equal(offer.note, "You can cancel until it starts. The whole reserve comes back.");
    const { shownCancel } = await import("./member-booking-card-copy.ts");
    const view = shownCancel(offer);
    assert.equal(view.visible, true);
    assert.equal(view.confirmText, offer.confirmText);
    assert.equal(view.note, offer.note);
    assert.equal(view.label, "Cancel");
    assert.equal(/\{cancel\?\.visible \? \(\s*<p className="muted">/.test(card), false);
  });
});
