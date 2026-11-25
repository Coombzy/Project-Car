import assert from "node:assert/strict";
import test from "node:test";
import { nextHourStart, endFromDuration, MAX_MEMBER_BOOKING_HOURS, MAX_SHOP_BOOKING_HOURS } from "./booking-defaults.ts";

test("nextHourStart snaps 19:59 to 20:00 and leaves 20:00 unchanged; endFromDuration adds whole hours", () => {
  const at1959 = new Date("2026-11-25T19:59:00");
  const at2000 = new Date("2026-11-25T20:00:00");
  assert.equal(nextHourStart(at1959).toISOString(), new Date("2026-11-25T20:00:00").toISOString());
  assert.equal(nextHourStart(at2000).toISOString(), at2000.toISOString());
  assert.equal(endFromDuration(at2000, 2).toISOString(), new Date("2026-11-25T22:00:00").toISOString());
  assert.equal(MAX_MEMBER_BOOKING_HOURS, 12);
  assert.equal(MAX_SHOP_BOOKING_HOURS, 24);
});
