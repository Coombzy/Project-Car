import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { describe, it } from "node:test";

const signup = readFileSync(new URL("../app/signup/page.tsx", import.meta.url), "utf8");
const actions = readFileSync(new URL("../app/signup/actions.ts", import.meta.url), "utf8");
const middleware = readFileSync(new URL("../middleware.ts", import.meta.url), "utf8");
const origin = readFileSync(new URL("./request-origin.ts", import.meta.url), "utf8");

describe("self-serve signup", () => {
  it("lets a new member set a password and pick Basic, with the waitlist as a fallback", () => {
    assert.match(signup, /name="password"/);
    assert.match(signup, /minLength=\{12\}/);
    assert.match(signup, /name="tier_name"/);
    assert.match(signup, /value="basic"/);
    assert.match(signup, /defaultChecked/);
    assert.match(signup, /You're on the waitlist\. We'll be in touch\./);
    assert.doesNotMatch(signup, /\$\d/);
    assert.match(actions, /\/signup/);
    assert.match(actions, /writeMemberSessionCookie/);
    assert.match(actions, /tier_name/);
    assert.match(middleware, /path === "\/signup"/);
    assert.match(origin, /pathname === "\/signup"/);
  });
});
