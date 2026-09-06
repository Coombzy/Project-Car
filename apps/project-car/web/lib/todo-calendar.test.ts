import assert from "node:assert/strict";
import { describe, it } from "node:test";

import { googleTemplateUrl, partsStatusLabel } from "./todo-calendar.ts";

describe("todo calendar helpers", () => {
  it("builds a Google template URL for a due date", () => {
    const url = googleTemplateUrl({
      title: "Call Priya",
      notes: "Waitlist",
      due_at: "2026-09-07T15:00:00-06:00",
    });
    assert.ok(url);
    assert.match(url, /calendar\.google\.com\/calendar\/render/);
    assert.match(url, /text=Call\+Priya/);
    assert.match(url, /ctz=America%2FRegina/);
  });

  it("returns null without a due date", () => {
    assert.equal(
      googleTemplateUrl({
        title: "No due",
        notes: null,
        due_at: null,
      }),
      null,
    );
  });

  it("labels parts statuses", () => {
    assert.equal(partsStatusLabel("in_transit"), "In transit");
    assert.equal(partsStatusLabel("ordered"), "ordered");
  });
});
