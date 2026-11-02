import assert from "node:assert/strict";
import { describe, it } from "node:test";

import { BOUNTY_ERROR, JOB_BOUNTY_CAP, TITLE_ERROR, parseJobForm } from "./job-form.ts";

describe("parseJobForm", () => {
  it("refuses a blank title", () => {
    for (const title of ["", "   ", "\n\t"]) {
      assert.deepEqual(parseJobForm({ title, notes: "", bounty: "25" }), {
        ok: false,
        error: TITLE_ERROR,
      });
    }
    assert.deepEqual(parseJobForm({ title: null, bounty: "25" }), {
      ok: false,
      error: TITLE_ERROR,
    });
  });

  it("accepts 0, 1.5 and 10000 and refuses -1, 1.555 and 10000.01", () => {
    assert.equal(JOB_BOUNTY_CAP, 10_000);
    assert.match(BOUNTY_ERROR, /0 to 10,000/);

    for (const bounty of ["0", "0.0", "0.00"]) {
      assert.deepEqual(parseJobForm({ title: "Sweep the bay", notes: "", bounty }), {
        ok: true,
        title: "Sweep the bay",
        notes: null,
        token_bounty: "0",
      });
    }

    assert.deepEqual(parseJobForm({ title: "Sweep the bay", bounty: "0.01" }), {
      ok: true,
      title: "Sweep the bay",
      notes: null,
      token_bounty: "0.01",
    });
    assert.deepEqual(parseJobForm({ title: "Sweep the bay", bounty: "0.10" }), {
      ok: true,
      title: "Sweep the bay",
      notes: null,
      token_bounty: "0.1",
    });
    assert.deepEqual(parseJobForm({ title: "Sweep the bay", bounty: "1.5" }), {
      ok: true,
      title: "Sweep the bay",
      notes: null,
      token_bounty: "1.5",
    });
    assert.deepEqual(parseJobForm({ title: "Sweep the bay", bounty: "2.50" }), {
      ok: true,
      title: "Sweep the bay",
      notes: null,
      token_bounty: "2.5",
    });
    assert.deepEqual(parseJobForm({ title: "Sweep the bay", bounty: "10000" }), {
      ok: true,
      title: "Sweep the bay",
      notes: null,
      token_bounty: "10000",
    });

    for (const bounty of ["-1", "1.555", "10000.01", "abc", ""]) {
      assert.deepEqual(parseJobForm({ title: "Sweep the bay", notes: "", bounty }), {
        ok: false,
        error: BOUNTY_ERROR,
      });
    }
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
