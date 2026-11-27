import assert from "node:assert/strict";
import test from "node:test";
import { icsHref } from "./booking-ics-link.ts";
test("icsHref: confirmed and pending get an encoded href; active, overdue, cancelled get none", () => {
  assert.equal(icsHref({ id: "a/b", status: "confirmed" }), "/member/bookings/a%2Fb/ics");
  assert.equal(icsHref({ id: "x", status: "pending" }), "/member/bookings/x/ics");
  for (const status of ["active", "overdue", "cancelled"]) {
    assert.equal(icsHref({ id: "x", status }), null);
  }
});
