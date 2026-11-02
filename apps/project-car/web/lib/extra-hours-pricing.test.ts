import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { describe, it } from "node:test";

import { extraHoursLine } from "./booking-calendar";

const detail = readFileSync(new URL("../components/ledger-detail.tsx", import.meta.url), "utf8");

describe("extra-hour pricing column", () => {
  it("fills the pricing column from the extra-hour line", () => {
    assert.equal(
      extraHoursLine({
        reason: "extra_hours",
        pricing: "1h × 100 × 1.00 = 100.00 · Normal + 1h × 100 × 1.25 = 125.00 · Evening",
      }),
      "1h × 100 × 1.00 = 100.00 · Normal + 1h × 100 × 1.25 = 125.00 · Evening",
    );
    assert.equal(extraHoursLine({ purchase: { subtotal_cad: "1.00" } }), null);
    assert.match(detail, /extraHoursLine/);
  });
});
