import assert from "node:assert/strict";
import { describe, it } from "node:test";
import { offersCancel } from "./booking-cancel.ts";

const CONTROLS = ["owner", "member-pending", "member-confirmed"] as const;

describe("booking cancel on an active visit", () => {
  it("test_active_cards_do_not_offer_cancel", () => {
    for (const control of CONTROLS) {
      assert.equal(offersCancel("active", control), false, control);
    }
    assert.equal(offersCancel("pending", "owner"), true);
    assert.equal(offersCancel("confirmed", "owner"), true);
    assert.equal(offersCancel("pending", "member-pending"), true);
    assert.equal(offersCancel("confirmed", "member-confirmed"), true);
    assert.equal(offersCancel("confirmed", "member-pending"), false);
    assert.equal(offersCancel("pending", "member-confirmed"), false);
  });
});
