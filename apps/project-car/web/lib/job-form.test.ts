import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

import { JOB_BOUNTY_CAP, parseJobForm } from "./job-form.ts";

const jobsApiPath = join(dirname(fileURLToPath(import.meta.url)), "jobs-api.ts");

const TITLE_ERROR = "Enter a title.";
const BOUNTY_ERROR =
  "A job bounty is 0 to 10,000 tokens, with at most two decimal places.";

function pathStrings(source: string): string[] {
  const paths: string[] = [];
  const re = /(["'`])((?:\\.|(?!\1)[\s\S])*?)\1/g;
  for (const match of source.matchAll(re)) {
    const body = match[2] ?? "";
    const quote = match[1] ?? "";
    if (body.startsWith("/") || (quote === "`" && body.includes("/"))) {
      paths.push(body);
    }
  }
  return paths;
}

/** Bare `${id}`, `${name}`, `${job_id}`, or `${jobId}`. `${pathSegment(...)}` is not bare. */
function hasBarePathInterpolation(path: string): boolean {
  return /\$\{(?:job_id|jobId|name|id)\}/.test(path);
}

describe("parseJobForm", () => {
  it("refuses a blank title", () => {
    for (const title of ["", "   ", "\n\t"]) {
      assert.deepEqual(parseJobForm({ title, notes: "", bounty: "25" }), {
        ok: false,
        error: TITLE_ERROR,
      });
    }
  });

  it("refuses -1, 1.555 and 10000.01", () => {
    for (const bounty of ["-1", "1.555", "10000.01", "abc"]) {
      assert.deepEqual(parseJobForm({ title: "Sweep the bay", notes: "", bounty }), {
        ok: false,
        error: BOUNTY_ERROR,
      });
    }
  });

  it("refuses a zero bounty", () => {
    for (const bounty of ["0", "0.0", "0.00"]) {
      assert.deepEqual(parseJobForm({ title: "Sweep the bay", notes: "", bounty }), {
        ok: false,
        error: BOUNTY_ERROR,
      });
    }
  });

  it("parses 0.01, 1.5 and 10000", () => {
    assert.equal(JOB_BOUNTY_CAP, 10_000);
    assert.deepEqual(parseJobForm({ title: "Sweep the bay", notes: "", bounty: "0.01" }), {
      ok: true,
      title: "Sweep the bay",
      notes: null,
      token_bounty: "0.01",
    });
    assert.deepEqual(parseJobForm({ title: "Sweep the bay", notes: "", bounty: "0.10" }), {
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

  it("jobs-api.ts paths reject a bare ${id}, ${name}, ${job_id} or ${jobId}", () => {
    const source = readFileSync(jobsApiPath, "utf8");
    const paths = pathStrings(source);
    assert.ok(
      paths.includes("/jobs"),
      `createShopJob must post a constant /jobs, saw ${paths.join(", ") || "(none)"}`,
    );
    for (const path of paths) {
      assert.equal(hasBarePathInterpolation(path), false, `path interpolates a bare id: ${path}`);
    }

    const bareSamples = [
      'shopJson<ShopJob>(`/jobs/${id}`, "Could not post the job.")',
      "shopJson<ShopJob>(`/jobs/${name}`)",
      "shopJson<ShopJob>(`/member/jobs/${job_id}`)",
      "shopJson<ShopJob>(`/jobs/${jobId}/done`)",
      "shopJson<ShopJob>(`/jobs/${pathSegment(id)}/notes/${name}`)",
    ];
    for (const sample of bareSamples) {
      const found = pathStrings(sample);
      assert.ok(
        found.some((path) => hasBarePathInterpolation(path)),
        `bare interpolation must fail: ${sample}`,
      );
    }

    const allowedSamples = [
      'shopJson<ShopJob>("/jobs", "Could not post the job.")',
      "shopJson<ShopJob>(`/member/jobs/${pathSegment(jobId)}/claim`)",
      "shopJson<ShopJob>(`/jobs/${pathSegment(id)}`)",
      "shopJson<ShopJob>(`/jobs/${pathSegment(name)}`)",
      "shopJson<ShopJob>(`/jobs/${pathSegment(job_id)}`)",
    ];
    for (const sample of allowedSamples) {
      const found = pathStrings(sample);
      assert.ok(found.length > 0, `no path in ${sample}`);
      for (const path of found) {
        assert.equal(hasBarePathInterpolation(path), false, `pathSegment path must pass: ${path}`);
      }
    }
  });
});
