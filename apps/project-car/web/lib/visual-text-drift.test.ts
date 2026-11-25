import assert from "node:assert/strict";
import { describe, it } from "node:test";

import { officialBodyDrift, OFFICIAL_1440_BODY } from "./visual-text-drift.ts";

describe("officialBodyDrift", () => {
  it("accepts the official frozen-clock body strings", () => {
    const source = [
      OFFICIAL_1440_BODY.tokensAtRisk,
      `Ada ${OFFICIAL_1440_BODY.adaTokens}`,
      ...OFFICIAL_1440_BODY.bands,
    ].join("\n");
    assert.deepEqual(officialBodyDrift(source), []);
  });

  it("rejects a #430-style drift that would sit under the 1% pixel cap", () => {
    assert.notEqual(
      officialBodyDrift("Tokens at risk 1\nAda 375\nOFF-PEAK\nNORMAL\nEVENING\nPEAK").length,
      0,
    );
  });
});
