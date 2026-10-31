import assert from "node:assert/strict";
import { existsSync, readFileSync } from "node:fs";
import { dirname, join, sep } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

import {
  JOB_BOUNTY_CAP,
  JOB_POST_FAILURE,
  JOB_POSTED_NOTICE,
  jobErrorHref,
  jobPostedHref,
  parseJobForm,
} from "./job-form.ts";

const actionsPath = join(dirname(fileURLToPath(import.meta.url)), "../app/jobs/actions.ts");
const BOUNTY_ERROR =
  "A job bounty is 0 to 10,000 tokens, with at most two decimal places.";

describe("postJobAction redirect", () => {
  it("keeps bounty 0, 1.5 and 10000 and refuses -1, 1.555 and 10000.01", () => {
    assert.equal(JOB_BOUNTY_CAP, 10_000);
    assert.deepEqual(parseJobForm({ title: "Sweep the bay", bounty: "0" }), {
      ok: true,
      title: "Sweep the bay",
      notes: null,
      token_bounty: "0",
    });
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

    const source = readFileSync(actionsPath, "utf8");
    assert.equal(source.includes("redirect(jobErrorHref(parsed.error))"), true);
    assert.equal(
      source.includes("error instanceof ShopApiError ? error.message : JOB_POST_FAILURE"),
      true,
    );
    assert.equal(source.includes("redirect(jobErrorHref(message))"), true);
    assert.match(source, /revalidatePath\("\/jobs"\);\s*redirect\(jobPostedHref\(\)\);/);
    assert.equal(source.includes("token_bounty: parsed.token_bounty"), true);
  });

  it("removes the visual scope lock without refusing bounty 0, 1.5 or 10000", () => {
    assert.equal(JOB_BOUNTY_CAP, 10_000);
    for (const [bounty, token] of [
      ["0", "0"],
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
