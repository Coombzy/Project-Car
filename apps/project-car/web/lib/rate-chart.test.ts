import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { describe, it } from "node:test";

import { cellColour, PEAK_CAP_NOTE } from "./rate-chart.ts";

describe("weekly rate chart", () => {
  it("colours each live band and keeps the peak-cap note", () => {
    assert.equal(cellColour("late_night"), "#6e7988");
    assert.equal(cellColour("weekday_day"), "#9fd19a");
    assert.equal(cellColour("weekday_eve"), "#c084fc");
    assert.equal(cellColour("weekend_fri_eve"), "#e8a54b");
    assert.equal(PEAK_CAP_NOTE, "Only Peak counts toward the 4-hour weekly cap.");

    const schedule = readFileSync(new URL("../app/member/schedule/page.tsx", import.meta.url), "utf8");
    const help = readFileSync(new URL("../app/member/help/page.tsx", import.meta.url), "utf8");
    assert.match(schedule, /RateChart/);
    assert.match(schedule, /getMemberRates/);
    assert.match(help, /RateChart/);
    assert.match(help, /getMemberRates/);
  });
});
