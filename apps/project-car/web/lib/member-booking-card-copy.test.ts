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

  it("cancel offer without confirmText/note has no empty note and labels Yes, cancel", async () => {
    const offer = memberCancelOffer(
      { status: "confirmed", startAt: "2026-11-07T16:00:00", reservedTokens: "80" },
      new Date("2026-11-05T22:00:00.000Z"),
    );
    const problems: string[] = [];
    if (!offer.visible) problems.push("offer not visible");
    if ("confirmText" in offer || "note" in offer) problems.push("offer already has confirm copy");
    if (/\{cancel\?\.visible \? \(\s*<p className="muted">/.test(card)) problems.push("empty muted note");
    try {
      const { shownCancel } = await import("./member-booking-card-copy.ts");
      const view = shownCancel(offer);
      if (view.confirmText !== "") problems.push("confirmText is present");
      if (view.note !== "") problems.push("note is present");
      if (view.label !== "Yes, cancel") problems.push(`label is ${view.label}`);
    } catch {
      problems.push("no shownCancel");
    }
    assert.deepEqual(problems, [], problems.join("; "));
  });
});
