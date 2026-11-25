import assert from "node:assert/strict";
import { describe, it } from "node:test";

import { OFFICIAL_1440_BODY, officialBodyDrift } from "./visual-text-drift.ts";

const STALE = [
  "Tokens at risk 3",
  "Ada 156.25",
  "WEEKDAY DAY (BASE)",
  "WEEKDAY EVENING",
  "WEEKEND / FRI EVE",
  "LATE NIGHT / EARLY MORNING",
].join("\n");

describe("officialBodyDrift", () => {
  it("accepts Tokens at risk 1, Ada 375.00, and the short bands", () => {
    assert.equal(OFFICIAL_1440_BODY.tokensAtRisk, "Tokens at risk 1");
    assert.equal(OFFICIAL_1440_BODY.adaTokens, "375.00");
    assert.deepEqual([...OFFICIAL_1440_BODY.bands], ["OFF-PEAK", "NORMAL", "EVENING", "PEAK"]);
    const body = [OFFICIAL_1440_BODY.tokensAtRisk, `Ada ${OFFICIAL_1440_BODY.adaTokens}`, ...OFFICIAL_1440_BODY.bands].join("\n");
    assert.deepEqual(officialBodyDrift(body), []);
  });

  it("counts 156.25, Tokens at risk 3, and the long band names as drift", () => {
    const drift = officialBodyDrift(STALE);
    for (const label of [
      "Tokens at risk 3",
      "156.25",
      "WEEKDAY DAY (BASE)",
      "WEEKDAY EVENING",
      "WEEKEND",
      "FRI EVE",
      "LATE NIGHT",
      "EARLY MORNING",
    ]) {
      assert.ok(drift.includes(label), label);
    }
  });
});
