import assert from "node:assert/strict";
import { existsSync } from "node:fs";
import { dirname, join, sep } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

import { ShopApiError } from "./config.ts";
import {
  JOB_BOUNTY_CAP,
  JOB_POST_FAILURE,
  JOB_POSTED_NOTICE,
  jobErrorHref,
  jobPostedHref,
  parseJobForm,
} from "./job-form.ts";
import { jobPostDecision } from "./job-post.ts";

const BOUNTY_ERROR =
  "A job bounty is 0 to 10,000 tokens, with at most two decimal places.";

describe("postJobAction redirect", () => {
  it("accepts bounty 0, 1.5 and 10000 and refuses -1, 1.555 and 10000.01", () => {
    assert.equal(JOB_BOUNTY_CAP, 10_000);
    for (const bounty of ["0", "0.0", "0.00"]) {
      assert.deepEqual(parseJobForm({ title: "Sweep the bay", bounty }), {
        ok: true,
        title: "Sweep the bay",
        notes: null,
        token_bounty: "0",
      });
    }
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
    for (const bounty of ["-1", "1.555", "10000.01"]) {
      assert.deepEqual(parseJobForm({ title: "Sweep the bay", bounty }), {
        ok: false,
        error: BOUNTY_ERROR,
      });
    }
  });

  it("redirects /jobs with a notice or the API error", () => {
    assert.equal(JOB_POSTED_NOTICE, "Job posted.");
    assert.equal(JOB_POST_FAILURE, "Could not post the job.");
    assert.equal(jobPostedHref(), `/jobs?notice=${encodeURIComponent(JOB_POSTED_NOTICE)}`);
    assert.equal(jobErrorHref(BOUNTY_ERROR), `/jobs?error=${encodeURIComponent(BOUNTY_ERROR)}`);
    assert.equal(jobErrorHref("a&b=c"), "/jobs?error=a%26b%3Dc");
    assert.equal(jobPostedHref(), "/jobs?notice=Job%20posted.");

    const rejected = { ok: false as const, error: "a&b=c" };
    assert.deepEqual(jobPostDecision({ type: "parsed", parsed: rejected }), {
      kind: "redirect",
      href: jobErrorHref(rejected.error),
    });

    const parsed = parseJobForm({ title: "Sweep the bay", notes: "  bay  ", bounty: "1.50" });
    assert.equal(parsed.ok, true);
    if (parsed.ok) {
      assert.equal(parsed.token_bounty, "1.5");
      assert.deepEqual(jobPostDecision({ type: "parsed", parsed }), {
        kind: "create",
        body: {
          title: "Sweep the bay",
          notes: "bay",
          token_bounty: parsed.token_bounty,
        },
      });
    }

    const apiError = new ShopApiError(400, "invalid", "Bounty is closed.");
    assert.deepEqual(jobPostDecision({ type: "rejected", error: apiError }), {
      kind: "redirect",
      href: jobErrorHref(apiError.message),
    });
    for (const error of [new Error("down"), "nope", { message: "secret" }]) {
      assert.deepEqual(jobPostDecision({ type: "rejected", error }), {
        kind: "redirect",
        href: jobErrorHref(JOB_POST_FAILURE),
      });
    }

    assert.deepEqual(jobPostDecision({ type: "created" }), {
      kind: "posted",
      revalidate: "/jobs",
      href: jobPostedHref(),
    });
  });

  it("removes the visual scope lock without refusing bounty 1.5 or 10000", () => {
    assert.equal(JOB_BOUNTY_CAP, 10_000);
    for (const [bounty, token] of [
      ["0", "0"],
      ["0.0", "0"],
      ["0.00", "0"],
      ["0.01", "0.01"],
      ["1.5", "1.5"],
      ["10000", "10000"],
      ["2.50", "2.5"],
    ] as const) {
      assert.deepEqual(parseJobForm({ title: "Sweep the bay", bounty }), {
        ok: true,
        title: "Sweep the bay",
        notes: null,
        token_bounty: token,
      });
    }
    for (const bounty of ["-1", "1.555", "10000.01"]) {
      assert.deepEqual(parseJobForm({ title: "Sweep the bay", bounty }), {
        ok: false,
        error: BOUNTY_ERROR,
      });
    }
    assert.equal(jobPostedHref(), "/jobs?notice=Job%20posted.");
    assert.equal(
      jobErrorHref(BOUNTY_ERROR),
      `/jobs?error=${encodeURIComponent(BOUNTY_ERROR)}`,
    );

    const scope = join(dirname(fileURLToPath(import.meta.url)), "../../api/tests/test_r80_scope.py");
    const marker = ["apps", "project-car", "api", "tests", "test_r80_scope.py"].join(sep);
    assert.equal(scope.endsWith(marker), true, scope);
    assert.equal(
      existsSync(scope),
      false,
      "R80 must not ship api/tests/test_r80_scope.py.",
    );
  });
});
