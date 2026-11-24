import assert from "node:assert/strict";
import { describe, it } from "node:test";
import { completeUnusedField } from "./booking-complete.ts";

const CLOSED = ["pending", "confirmed", "completed", "overdue", "cancelled"] as const;

describe("owner complete booking", () => {
  it("test_complete_card_posts_owner_unused_tokens", () => {
    const field = completeUnusedField("active", "12.50");
    assert.ok(field);
    assert.equal(field.type, "number");
    assert.equal(field.name, "unused_tokens");
    assert.equal(field.defaultValue, 0);
    assert.equal(field.min, 0);
    assert.equal(field.max, "12.50");
    assert.equal(field.step, "0.01");
    assert.equal("value" in field, false);

    assert.equal(completeUnusedField("active", "0")?.max, "0");
    for (const status of CLOSED) {
      assert.equal(completeUnusedField(status, "12.50"), null, status);
    }
  });
});
