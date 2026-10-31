import assert from "node:assert/strict";
import { describe, it } from "node:test";

import { dashboardHref } from "./error-pages.ts";

describe("dashboard href path normalization", () => {
  it("test_normalized_pathname_picks_the_dashboard", () => {
    // Dot segments are owner paths. The prefix check on the raw string
    // still returns /member for these, which is the wrong dashboard.
    assert.equal(dashboardHref("/member/../schedule"), "/");
    assert.equal(dashboardHref("/member/%2e%2e/schedule"), "/");
    assert.equal(dashboardHref("/member/%2E%2E/%2e%2e/login"), "/");
    assert.equal(dashboardHref("/member/nope/../../schedule"), "/");

    // A path that only looks like /members or /membership can still resolve
    // into the member area.
    assert.equal(dashboardHref("/members/../member/nope"), "/member");
    assert.equal(dashboardHref("/membership/../member/schedule"), "/member");

    assert.equal(dashboardHref("/member"), "/member");
    assert.equal(dashboardHref("/member/"), "/member");
    assert.equal(dashboardHref("/member/nope"), "/member");
    assert.equal(dashboardHref("/member/schedule"), "/member");
    assert.equal(dashboardHref("/members/missing"), "/");
    assert.equal(dashboardHref("/membership"), "/");
    assert.equal(dashboardHref("/no-such-page"), "/");
    assert.equal(dashboardHref("/schedul"), "/");
    assert.equal(dashboardHref("/_not-found"), "/");
    assert.equal(dashboardHref(""), "/");
  });
});
