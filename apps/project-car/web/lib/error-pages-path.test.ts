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

  it("test_non_path_strings_stay_on_the_owner_dashboard", () => {
    // new URL(pathname, base) follows a scheme or a protocol-relative prefix
    // and resolves a relative string against that base. Neither is
    // window.location.pathname. Those strings must not become /member.
    assert.equal(dashboardHref("https://shop.example/member/nope"), "/");
    assert.equal(dashboardHref("http://shop.invalid/member/schedule"), "/");
    assert.equal(dashboardHref("//shop.example/member/nope"), "/");
    assert.equal(dashboardHref("//member/nope"), "/");
    assert.equal(dashboardHref("member/nope"), "/");
    assert.equal(dashboardHref("\\member\\nope"), "/");

    assert.equal(dashboardHref("/member/nope"), "/member");
    assert.equal(dashboardHref("/member/../schedule"), "/");
    assert.equal(dashboardHref("/no-such-page"), "/");
  });

  it("test_backslash_protocol_relative_stays_on_the_owner_dashboard", () => {
    // `/\evil.com\member\nope` starts with one slash, so the `//` guard misses it.
    // The URL parser rewrites `\` to `/` and takes evil.com as the host. That is
    // not window.location.pathname. It must not follow the path to /member.
    assert.equal(dashboardHref("/\\evil.com\\member\\nope"), "/");
    assert.equal(dashboardHref("/\\@evil\\member\\nope"), "/");
    assert.equal(dashboardHref("/\\/member/nope"), "/");

    assert.equal(dashboardHref("/member/nope"), "/member");
    assert.equal(dashboardHref("/member/../schedule"), "/");
    assert.equal(dashboardHref("/no-such-page"), "/");
  });

  it("test_backslash_parse_base_stays_on_the_owner_dashboard", () => {
    // `/\shop.invalid\member\nope` starts with one slash, so the `//` guard misses it.
    // new URL rewrites `\` to `/` and the host stays the parse base shop.invalid,
    // so a host check still follows the path to /member. A raw backslash is not
    // window.location.pathname.
    assert.equal(dashboardHref("/\\shop.invalid\\member\\nope"), "/");
    assert.equal(dashboardHref("/\\SHOP.INVALID\\member\\nope"), "/");
    assert.equal(dashboardHref("/\\user@shop.invalid\\member\\nope"), "/");
    assert.equal(dashboardHref("/\\shop.invalid:443\\member\\nope"), "/");

    assert.equal(dashboardHref("/member/nope"), "/member");
    assert.equal(dashboardHref("/member/../schedule"), "/");
    assert.equal(dashboardHref("/no-such-page"), "/");
  });

  it("test_control_character_pathname_stays_on_the_owner_dashboard", () => {
    // window.location.pathname percent-encodes controls. A raw tab, newline,
    // CR, NUL, or DEL is not that pathname. The URL parser deletes the
    // C0 controls, so these strings look like /member/... and would link
    // to the member dashboard.
    assert.equal(dashboardHref("/member\u0009/nope"), "/");
    assert.equal(dashboardHref("/member\u000a/nope"), "/");
    assert.equal(dashboardHref("/member\u000d/schedule"), "/");
    assert.equal(dashboardHref("/\u0009member/nope"), "/");
    assert.equal(dashboardHref("/member/nope\u0000"), "/");
    assert.equal(dashboardHref("/member/nope\u007f"), "/");

    assert.equal(dashboardHref("/member/nope"), "/member");
    assert.equal(dashboardHref("/member/schedule"), "/member");
    assert.equal(dashboardHref("/member/../schedule"), "/");
    assert.equal(dashboardHref("/no-such-page"), "/");
    assert.equal(dashboardHref("/%09/member/nope"), "/");
  });
});
