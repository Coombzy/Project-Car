import assert from "node:assert/strict";
import { describe, it } from "node:test";

import { JOB_BOUNTY_CAP, parseJobForm } from "./job-form.ts";

const TITLE_ERROR = "Enter a title.";
const BOUNTY_ERROR =
  "A job bounty is above 0 and at most 10,000 tokens, with at most two decimal places.";

describe("parseJobForm", () => {
  it("refuses a blank title", () => {
    for (const title of ["", "   ", "\n\t"]) {
      assert.deepEqual(parseJobForm({ title, notes: "", bounty: "25" }), {
        ok: false,
        error: TITLE_ERROR,
      });
    }
  });

  it("refuses bounty 0, 1.555 and 10000.01", () => {
    for (const bounty of ["0", "1.555", "10000.01"]) {
      assert.deepEqual(parseJobForm({ title: "Sweep the bay", bounty }), {
        ok: false,
        error: BOUNTY_ERROR,
      });
    }
  });

  it("parses 1.5 and 10000", () => {
    assert.equal(JOB_BOUNTY_CAP, 10_000);
    assert.deepEqual(parseJobForm({ title: "Sweep the bay", bounty: "1.5" }), {
      ok: true,
      title: "Sweep the bay",
      notes: null,
      token_bounty: "1.5",
    });
    assert.deepEqual(parseJobForm({ title: "Sweep the bay", bounty: "10000" }), {
      ok: true,
      title: "Sweep the bay",
      notes: null,
      token_bounty: "10000",
    });
    assert.deepEqual(parseJobForm({ title: "Sweep the bay", bounty: "2.50" }), {
      ok: true,
      title: "Sweep the bay",
      notes: null,
      token_bounty: "2.5",
    });
  });

  it("parses a good form and trims the title", () => {
    assert.deepEqual(
      parseJobForm({
        title: "  Sweep the bay  ",
        notes: "  after close  ",
        bounty: " 25 ",
      }),
      { ok: true, title: "Sweep the bay", notes: "after close", token_bounty: "25" },
    );
    assert.deepEqual(parseJobForm({ title: "Oil the hoist", notes: "   ", bounty: "1" }), {
      ok: true,
      title: "Oil the hoist",
      notes: null,
      token_bounty: "1",
    });
  });
});
