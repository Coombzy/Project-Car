import assert from "node:assert/strict";
import { describe, it } from "node:test";

import { lowestFreeBay, type BayChoice, type SpanInterval } from "./booking-calendar.ts";

const bays: BayChoice[] = [
  { id: "bay-1", name: "Bay 1", number: 1, isShop: false, status: "available" },
  { id: "bay-2", name: "Bay 2", number: 2, isShop: false, status: "available" },
];

const start = "2026-06-18T14:00:00";
const end = "2026-06-18T16:00:00";

function span(status: string): SpanInterval {
  return { hoistId: "bay-1", startAt: start, endAt: end, status };
}

describe("lowestFreeBay", () => {
  it("test_completed_visit_leaves_that_bay_free", () => {
    assert.equal(lowestFreeBay(bays, [span("completed")], start, end)?.id, "bay-1");
    assert.equal(lowestFreeBay(bays, [span("confirmed")], start, end)?.id, "bay-2");
    assert.equal(lowestFreeBay(bays, [span("pending")], start, end)?.id, "bay-2");
    assert.equal(lowestFreeBay(bays, [span("active")], start, end)?.id, "bay-2");
    assert.equal(lowestFreeBay(bays, [span("overdue")], start, end)?.id, "bay-2");
  });
});
