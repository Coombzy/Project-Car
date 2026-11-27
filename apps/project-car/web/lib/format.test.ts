import assert from "node:assert/strict";
import { describe, it } from "node:test";

import { formatHours, ledgerKindLabel, tierName } from "./format.ts";

describe("R124 format helpers", () => {
  it("R124 formatHours trims trailing zeros and appends h", () => {
    assert.equal(formatHours("65.0000"), "65 h");
    assert.equal(formatHours("1.5000"), "1.5 h");
    assert.equal(formatHours("0.0000"), "0 h");
    assert.equal(formatHours("2"), "2 h");
  });

  it("R124 tierName returns the matching name or the slug", () => {
    const tiers = [
      { slug: "basic", name: "Basic" },
      { slug: "premium", name: "Premium" },
    ];
    assert.equal(tierName("premium", tiers), "Premium");
    assert.equal(tierName("unknown-tier", tiers), "unknown-tier");
  });

  it("R124 ledgerKindLabel names every TokenTransactionKind", () => {
    assert.equal(ledgerKindLabel("booking_reserve"), "Booking hold");
    assert.equal(ledgerKindLabel("booking_debit"), "Booking debit");
    assert.equal(ledgerKindLabel("booking_refund"), "Booking refund");
    assert.equal(ledgerKindLabel("monthly_allocation"), "Monthly grant");
    assert.equal(ledgerKindLabel("admin_adjustment"), "Owner adjustment");
    assert.equal(ledgerKindLabel("token_purchase"), "Token purchase");
    assert.equal(ledgerKindLabel("mystery_kind"), "mystery_kind");
  });
});
