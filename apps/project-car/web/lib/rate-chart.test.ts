import assert from "node:assert/strict";
import { describe, it } from "node:test";
import { resolve } from "./extension-hook.mjs";
import { PEAK_CAP_NOTE, cellColour } from "./rate-chart.ts";

describe("PC #282 part 6/11 rate chart", () => {
  it("loads the peak-cap note and band colours", () => {
    assert.equal(PEAK_CAP_NOTE, "Only Peak counts toward the 4-hour weekly cap.");
    assert.equal(cellColour("late_night"), "#6e7988");
    assert.equal(cellColour("weekday_day"), "#9fd19a");
    assert.equal(cellColour("weekday_eve"), "#c084fc");
    assert.equal(cellColour("weekend_fri_eve"), "#e8a54b");
    assert.equal(cellColour("fill"), "#f3f0e8");
  });

  it("appends .ts for an extensionless relative specifier", async () => {
    const seen: string[] = [];
    const next = async (specifier: string) => {
      seen.push(specifier);
      return { url: specifier };
    };
    await resolve("./rate-chart", {}, next);
    await resolve("../calendar", {}, next);
    await resolve("./rate-chart.ts", {}, next);
    assert.deepEqual(seen, ["./rate-chart.ts", "../calendar.ts", "./rate-chart.ts"]);
  });
});
