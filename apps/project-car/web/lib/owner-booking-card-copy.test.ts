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

  it("posts unused tokens from completeUnusedField on the finish form", () => {
    assert.match(card, /import \{ completeUnusedField \} from "\.\.\/lib\/booking-complete"/);
    assert.match(card, /const unused = completeUnusedField\(booking\.status, booking\.reserved_tokens\)/);
    assert.match(card, /\{unused \? \(/);
    assert.match(card, /className="unused-tokens"/);
    assert.match(card, /<input \{\.\.\.unused\} inputMode="decimal" \/>/);
    assert.equal(card.includes("Finish visit"), false);
    assert.equal(card.includes('name="reason"'), false);
  });

  it("cancels through offersCancel without a required reason", () => {
    assert.match(card, /import \{ offersCancel \} from "\.\.\/lib\/booking-cancel"/);
    assert.match(card, /\{offersCancel\(booking\.status, "owner"\) \? \(/);
    assert.equal(card.includes("Reason"), false);
    assert.equal(card.includes("minLength"), false);
    assert.match(card, /action=\{confirmBookingAction\}/);
    assert.match(card, /action=\{checkInBookingAction\}/);
    assert.match(card, /checkInButtonState\(booking\.start_at, shopClock\(\), booking\.end_at\)/);
  });
});
