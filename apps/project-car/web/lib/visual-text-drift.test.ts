import assert from "node:assert/strict";
import { describe, it } from "node:test";

import { OFFICIAL_1440_BODY, officialBodyDrift } from "./visual-text-drift.ts";

/** Live frozen-clock copy. Ada's ledger balance is 375.00. */
const OFFICIAL_BODY = [
  "Tokens at risk 1",
  "Ada 375.00",
  "OFF-PEAK",
  "NORMAL",
  "EVENING",
  "PEAK",
].join("\n");

/** Pre-#284 seed copy. These phrases are drift under the frozen clock. */
const STALE_BODY = [
  "Tokens at risk 3",
  "Ada 156.25",
  "WEEKDAY DAY (BASE)",
  "WEEKDAY EVENING",
  "WEEKEND / FRI EVE",
  "LATE NIGHT / EARLY MORNING",
].join("\n");

const STALE_HITS = [
  "Tokens at risk 3",
  "156.25",
  "WEEKDAY DAY (BASE)",
  "WEEKDAY EVENING",
  "WEEKEND",
  "FRI EVE",
  "LATE NIGHT",
  "EARLY MORNING",
] as const;

describe("officialBodyDrift", () => {
  it("locks the official frozen-clock strings", () => {
    assert.equal(OFFICIAL_1440_BODY.tokensAtRisk, "Tokens at risk 1");
    assert.equal(OFFICIAL_1440_BODY.adaTokens, "375.00");
    assert.deepEqual([...OFFICIAL_1440_BODY.bands], ["OFF-PEAK", "NORMAL", "EVENING", "PEAK"]);
  });

  it("accepts the official frozen-clock body strings", () => {
    assert.deepEqual(officialBodyDrift(OFFICIAL_BODY), []);
  });

  it("counts pre-#284 seed strings as drift", () => {
    const drift = officialBodyDrift(STALE_BODY);
    for (const label of STALE_HITS) {
      assert.ok(drift.includes(label), label);
    }
  });
});
