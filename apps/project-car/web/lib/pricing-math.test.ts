import assert from "node:assert/strict";
import { describe, it } from "node:test";

import { reserveFactors } from "./pricing-math.ts";

describe("reserve equation", () => {
  it("sums each held hour when the bands differ", () => {
    const factors = reserveFactors({
      hours: "6",
      band_multiplier: "1.21",
      advance_multiplier: "1",
      final_reserve_cost: "725.00",
      segments: [
        { band_tokens: "100" },
        { band_tokens: "125" },
        { band_tokens: "125" },
        { band_tokens: "125" },
        { band_tokens: "125" },
        { band_tokens: "125" },
      ],
    });
    assert.equal(factors, "100 + 125 + 125 + 125 + 125 + 125");
  });

  it("keeps one band as hours times that band", () => {
    const factors = reserveFactors({
      hours: "2",
      band_multiplier: "1.25",
      advance_multiplier: "1",
      final_reserve_cost: "250.00",
      segments: [{ band_tokens: "125" }, { band_tokens: "125" }],
    });
    assert.equal(factors, "2h × 100 × 1.25 × 1");
  });

  it("multiplies a mixed visit by fill without the last-minute overlay", () => {
    const factors = reserveFactors({
      hours: "2",
      band_multiplier: "1.13",
      advance_multiplier: "1",
      fill_multiplier: "0.75",
      final_reserve_cost: "168.75",
      segments: [{ band_tokens: "100" }, { band_tokens: "125" }],
    });
    assert.equal(factors, "(100 + 125) × 0.75");
  });
});
