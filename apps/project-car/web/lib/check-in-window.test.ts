import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";
import {
  CHECK_IN_EARLY_HINT,
  CHECK_IN_EARLY_MINUTES,
  CHECK_IN_ENDED_HINT,
  checkInButtonState,
} from "./check-in-window.ts";

const libDir = dirname(fileURLToPath(import.meta.url));
const cardPath = join(libDir, "../components/owner-booking-card.tsx");

function confirmedCheckInForm(source: string): string {
  const action = source.indexOf("action={checkInBookingAction}");
  assert.notEqual(action, -1, "check-in action is missing");
  const formStart = source.lastIndexOf("<form", action);
  assert.notEqual(formStart, -1, "confirmed booking has no check-in form");
  const formEnd = source.indexOf("</form>", action);
  assert.notEqual(formEnd, -1, "confirmed check-in form is unclosed");
  return source.slice(formStart, formEnd + "</form>".length);
}

describe("owner check-in window", () => {
  it("test_check_in_button_stays_closed_until_the_window", () => {
    const card = readFileSync(cardPath, "utf8");
    const form = confirmedCheckInForm(card);
    assert.match(
      form,
      /disabled=\{checkIn\.disabled\}/,
      "confirmed Check in must be disabled until the window opens",
    );
    assert.match(form, /\{checkIn\.hint\}/, "confirmed Check in must show the early hint");
    assert.match(
      card,
      /checkInButtonState\(booking\.start_at,\s*shopClock\(\),\s*booking\.end_at\)/,
      "confirmed Check in must close from the visit end",
    );

    assert.equal(CHECK_IN_EARLY_MINUTES, 15);
    assert.equal(CHECK_IN_EARLY_HINT, "Opens 15 min before start");
    assert.equal(CHECK_IN_ENDED_HINT, "Window ended");

    const now = new Date("2026-10-20T18:00:00.000Z");
    const at = (ms: number) => new Date(now.getTime() + ms).toISOString();
    const minute = 60 * 1000;

    const threeHours = checkInButtonState(at(3 * 60 * minute), now);
    assert.equal(threeHours.disabled, true);
    assert.equal(threeHours.hint, "Opens 15 min before start");

    const tenMinutes = checkInButtonState(at(10 * minute), now);
    assert.equal(tenMinutes.disabled, false);
    assert.equal(tenMinutes.hint, null);

    const fifteen = checkInButtonState(at(15 * minute), now);
    assert.equal(fifteen.disabled, false, "check-in opens at exactly 15 minutes before start");
    assert.equal(fifteen.hint, null);

    const justOver = checkInButtonState(at(15 * minute + 1), now);
    assert.equal(justOver.disabled, true);
    assert.equal(justOver.hint, "Opens 15 min before start");

    const started = checkInButtonState(at(-minute), now);
    assert.equal(started.disabled, false);
    assert.equal(started.hint, null);
  });

  it("test_check_in_button_closes_when_the_window_has_ended", () => {
    const card = readFileSync(cardPath, "utf8");
    const now = new Date("2026-10-20T18:00:00.000Z");
    const at = (ms: number) => new Date(now.getTime() + ms).toISOString();
    const minute = 60 * 1000;

    const hoursAfter = checkInButtonState(at(-3 * 60 * minute), now, at(-2 * 60 * minute));
    assert.equal(hoursAfter.hint, "Window ended");
    assert.equal(hoursAfter.disabled, true, "a confirmed no-show after the end stays closed");

    const atEnd = checkInButtonState(at(-60 * minute), now, at(0));
    assert.equal(atEnd.hint, "Window ended");
    assert.equal(atEnd.disabled, true, "check-in closes at the visit end");

    const beforeEnd = checkInButtonState(at(-60 * minute), now, at(1));
    assert.equal(beforeEnd.disabled, false, "check-in stays open until the visit end");
    assert.equal(beforeEnd.hint, null);

    const fifteen = checkInButtonState(at(15 * minute), now, at(75 * minute));
    assert.equal(fifteen.disabled, false, "an end still ahead does not move the early open");
    assert.equal(fifteen.hint, null);

    const justOver = checkInButtonState(at(15 * minute + 1), now, at(75 * minute));
    assert.equal(justOver.disabled, true);
    assert.equal(justOver.hint, "Opens 15 min before start");

    assert.match(
      card,
      /checkInButtonState\(booking\.start_at,\s*shopClock\(\),\s*booking\.end_at\)/,
      "owner card must pass the visit end into the check-in window",
    );
  });
});
