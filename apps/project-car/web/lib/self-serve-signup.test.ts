import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { describe, it } from "node:test";

const signup = readFileSync(new URL("../app/signup/page.tsx", import.meta.url), "utf8");
const members = readFileSync(new URL("../app/members/page.tsx", import.meta.url), "utf8");
const waitlist = readFileSync(new URL("../app/waitlist/page.tsx", import.meta.url), "utf8");

describe("self-serve signup", () => {
  it("lets a new member set a password and pick Basic, with the waitlist as a fallback", () => {
    assert.match(signup, /name="password"/);
    assert.match(signup, /minLength=\{12\}/);
    assert.match(signup, /tier_name/);
    assert.match(signup, /basic/);
    assert.match(signup, /listPublicPlans/);
    assert.match(signup, /Waitlist/);
    assert.doesNotMatch(signup, /\$500|\$750/);
    assert.match(members, /\/signup/);
    assert.doesNotMatch(members, /self-serve signup is/);
    assert.match(waitlist, /signup-mode|signupMode|Waitlist fallback/);
  });
});
