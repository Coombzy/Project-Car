import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

const card = readFileSync(
  join(dirname(fileURLToPath(import.meta.url)), "../components/owner-booking-card.tsx"),
  "utf8",
);

describe("owner booking card copy", () => {
  it("shows a Shop pill, Mountain Time, and bookingStatusLabel", () => {
    assert.match(card, /<span className="pill pill-shop">Shop<\/span>/);
    assert.match(card, /\{formatCalendarTime\(booking\.end_at\)\} · Mountain Time/);
    assert.match(card, /import \{ bookingStatusLabel \} from "\.\.\/lib\/booking-words"/);
    assert.match(
      card,
      /<span className=\{`pill pill-\$\{booking\.status\}`\}>\{bookingStatusLabel\(booking\.status\)\}<\/span>/,
    );
    assert.equal(card.includes("StatusPill"), false);
  });

  it("finishes an active or overdue visit without an unused-tokens field", () => {
    assert.match(card, /booking\.status === "active" \|\| booking\.status === "overdue"/);
    assert.match(card, />Finish visit</);
    assert.match(card, /Time past the booked end is charged by the hour\./);
    assert.equal(card.includes("Unused"), false);
    assert.equal(card.includes("completeUnusedField"), false);
  });

  it("requires a cancel reason and keeps confirm and check-in", () => {
    assert.match(card, /booking\.status === "pending" \|\| booking\.status === "confirmed"/);
    assert.match(card, />\s*Reason\s*<input type="text" name="reason" required minLength=\{3\} maxLength=\{500\} \/>/);
    assert.equal(card.includes("offersCancel"), false);
    assert.match(card, /action=\{confirmBookingAction\}/);
    assert.match(card, /action=\{checkInBookingAction\}/);
    assert.match(card, /checkInButtonState\(booking\.start_at, shopClock\(\), booking\.end_at\)/);
  });
});
