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

  it("does not let a known longer label satisfy a shorter band", () => {
    const official = "Tokens at risk 1\nAda 375.00\nOFF-PEAK\nNORMAL\nEVENING\nPEAK";
    assert.ok(!officialBodyDrift(official.replace("EVENING", "Band EVENING")).includes("EVENING"));
    assert.ok(officialBodyDrift(`${official}\nx WEEKEND`).includes("WEEKEND"));
    const weekday = officialBodyDrift("WEEKDAY EVENING");
    assert.ok(weekday.includes("EVENING") && weekday.includes("WEEKDAY EVENING"));
    assert.ok(officialBodyDrift("OFF-PEAK").includes("PEAK"));
    assert.ok(officialBodyDrift("Tokens at risk 1\nAda 375.00\nOFF-PEAK\nNORMAL\nEVENING").includes("PEAK"));
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
