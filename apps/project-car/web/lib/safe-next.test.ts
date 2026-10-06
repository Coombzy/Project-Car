import assert from "node:assert/strict";
import { describe, it } from "node:test";

import { safeMemberNext, safeOwnerNext } from "./safe-next.ts";

describe("safeOwnerNext", () => {
  it("test_safe_owner_next_rejects_off_site", () => {
    assert.equal(safeOwnerNext("/\\evil.example"), "/");
    assert.equal(safeOwnerNext("/\\\\host"), "/");
    assert.equal(safeOwnerNext("//host"), "/");
    assert.equal(safeOwnerNext("https://evil.example"), "/");
    assert.equal(safeOwnerNext("http://evil.example/schedule"), "/");
    assert.equal(safeOwnerNext("javascript:alert(1)"), "/");
    assert.equal(safeOwnerNext("/%2f%2fevil.example"), "/");
    assert.equal(safeOwnerNext("/%2F%2Fevil.example"), "/");
    assert.equal(safeOwnerNext("/%5cevil.example"), "/");
    assert.equal(safeOwnerNext("/%5C%5Chost"), "/");
    assert.equal(safeOwnerNext("/%252f%252fevil.example"), "/");
    assert.equal(safeOwnerNext("/%09/evil.example"), "/");
    assert.equal(safeOwnerNext("/schedule\\evil"), "/");
    assert.equal(safeOwnerNext("\\\\evil.example"), "/");
    assert.equal(safeOwnerNext(" /schedule"), "/");
    assert.equal(safeOwnerNext(""), "/");
    assert.equal(safeOwnerNext(undefined), "/");

    assert.equal(safeOwnerNext("/schedule"), "/schedule");
    assert.equal(safeOwnerNext("/"), "/");
    assert.equal(safeOwnerNext("/members"), "/members");
    assert.equal(safeOwnerNext("/member/schedule"), "/member/schedule");
    assert.equal(safeOwnerNext("/schedule?view=week"), "/schedule?view=week");
  });
});

describe("safeMemberNext", () => {
  it("test_safe_member_next_rejects_owner_members_path", () => {
    assert.equal(safeMemberNext("/members"), "/member");
    assert.equal(safeMemberNext("/membership"), "/member");
    assert.equal(safeMemberNext("/members/1"), "/member");
    assert.equal(safeMemberNext("/member/../schedule"), "/member");
    assert.equal(safeMemberNext("/member/%2e%2e/schedule"), "/member");
    assert.equal(safeMemberNext("/member/%2f%2e%2e%2fschedule"), "/member");
    assert.equal(safeMemberNext("//host"), "/member");
    assert.equal(safeMemberNext("/\\evil.example"), "/member");
    assert.equal(safeMemberNext("/\\\\host"), "/member");
    assert.equal(safeMemberNext("https://evil.example"), "/member");
    assert.equal(safeMemberNext("/%2f%2fevil.example"), "/member");
    assert.equal(safeMemberNext("/%5cevil.example"), "/member");
    assert.equal(safeMemberNext("/schedule"), "/member");
    assert.equal(safeMemberNext(""), "/member");
    assert.equal(safeMemberNext(undefined), "/member");

    assert.equal(safeMemberNext("/member"), "/member");
    assert.equal(safeMemberNext("/member/"), "/member/");
    assert.equal(safeMemberNext("/member/schedule"), "/member/schedule");
    assert.equal(safeMemberNext("/member/schedule?view=week"), "/member/schedule?view=week");
  });
});
