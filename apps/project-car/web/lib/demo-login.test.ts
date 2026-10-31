import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

import { showDemoLoginHints } from "./demo-login.ts";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");

describe("showDemoLoginHints", () => {
  it("is false in production when the flag is unset", () => {
    assert.equal(showDemoLoginHints({ NODE_ENV: "production" }), false);
  });

  it("is true in production when the flag is true", () => {
    assert.equal(
      showDemoLoginHints({ NODE_ENV: "production", SHOP_DEMO_LOGIN_HINTS: "true" }),
      true,
    );
  });

  it("is true outside production", () => {
    assert.equal(showDemoLoginHints({ NODE_ENV: "development" }), true);
  });
});

it("login screens reference the hint helper and do not hard-code the demo password", () => {
  const files = [
    "app/login/page.tsx",
    "app/login/login-form.tsx",
    "app/member/login/page.tsx",
    "app/member/login/login-form.tsx",
  ];
  for (const file of files) {
    const text = readFileSync(join(root, file), "utf8");
    assert.match(text, /showDemoLoginHints/);
    assert.equal(text.includes("changeme"), false, file);
  }
});
