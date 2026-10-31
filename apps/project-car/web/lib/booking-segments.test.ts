import assert from "node:assert/strict";
import { describe, it } from "node:test";

import type { PricingRule } from "./config.ts";
import {
  pricingRuleSummary,
  quoteSegmentLines,
  segmentCostLines,
  showSingleBandLabel,
} from "./booking-segments.ts";

const spanning: PricingRule = {
  band_id: "late_night",
  band_label: "Late night / early morning",
  band_multiplier: "0.75",
  overlay_id: "advance",
  overlay_label: "Advance",
  advance_multiplier: "0.85",
  hours: "14",
  base_tokens: "1400",
  final_reserve_cost: "1275.00",
  tz: "America/Regina",
  segments: [
    {
      band_id: "late_night",
      band_label: "Late night / early morning",
      band_multiplier: "0.75",
      start: "2026-09-07T07:00:00-06:00",
      end: "2026-09-07T08:00:00-06:00",
      hours: "1",
      tokens: "63.75",
    },
    {
      band_id: "weekday_day",
      band_label: "Weekday day (base)",
      band_multiplier: "1",
      start: "2026-09-07T08:00:00-06:00",
      end: "2026-09-07T16:00:00-06:00",
      hours: "8",
      tokens: "680",
    },
    {
      band_id: "weekday_eve",
      band_label: "Weekday evening",
      band_multiplier: "1.25",
      start: "2026-09-07T16:00:00-06:00",
      end: "2026-09-07T21:00:00-06:00",
      hours: "5",
      tokens: "531.25",
    },
  ],
};

const singleBand: PricingRule = {
  band_id: "weekday_day",
  band_label: "Weekday day (base)",
  band_multiplier: "1",
  overlay_id: "standard",
  overlay_label: "Standard",
  advance_multiplier: "1",
  hours: "2",
  base_tokens: "200",
  final_reserve_cost: "200.00",
  tz: "America/Regina",
  segments: [
    {
      band_id: "weekday_day",
      band_label: "Weekday day (base)",
      band_multiplier: "1",
      start: "2026-09-08T09:00:00-06:00",
      end: "2026-09-08T11:00:00-06:00",
      hours: "2",
      tokens: "200",
    },
  ],
};

describe("segment cost lines", () => {
  it("test_spanning_booking_lists_each_band_and_the_total", () => {
    const lines = segmentCostLines(spanning);
    assert.deepEqual(lines, [
      "Late night / early morning · 1h × 0.75 · 63.75",
      "Weekday day (base) · 8h × 1 · 680",
      "Weekday evening · 5h × 1.25 · 531.25",
    ]);
    assert.deepEqual(quoteSegmentLines(spanning), [...lines, "Total · 1275.00"]);
    assert.equal(showSingleBandLabel(spanning), false);
    const summary = pricingRuleSummary(spanning);
    assert.equal(summary.includes("Late night / early morning · 1h × 0.75 · 63.75"), true);
    assert.equal(summary.includes("Weekday evening · 5h × 1.25 · 531.25"), true);
    assert.equal(summary.includes("Total · 1275.00"), true);
    assert.equal(summary.startsWith("14h × 100 × 0.75"), false);
  });

  it("test_single_band_keeps_the_start_band_sentence", () => {
    assert.equal(showSingleBandLabel(singleBand), true);
    assert.equal(segmentCostLines(singleBand).length, 1);
    assert.equal(
      pricingRuleSummary(singleBand),
      "2h × 100 × 1 × 1 = 200 · Weekday day (base) · Standard",
    );
  });
});
