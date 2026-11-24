import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { afterEach, test } from "node:test";
import { join } from "node:path";

import { showDemoLoginHints } from "./demo-login.ts";

const webRoot = join(import.meta.dirname, "..");

afterEach(() => {
  delete process.env.SHOP_DEMO_LOGIN_HINTS;
});

test("showDemoLoginHints is true only when SHOP_DEMO_LOGIN_HINTS=true", () => {
  const previousNodeEnv = process.env.NODE_ENV;
  delete process.env.SHOP_DEMO_LOGIN_HINTS;
  try {
    process.env.NODE_ENV = "production";
    assert.equal(showDemoLoginHints(), false);
    process.env.NODE_ENV = "development";
    assert.equal(showDemoLoginHints(), false);
    process.env.SHOP_DEMO_LOGIN_HINTS = "1";
    assert.equal(showDemoLoginHints(), false);
    process.env.SHOP_DEMO_LOGIN_HINTS = "true";
    assert.equal(showDemoLoginHints(), true);
  } finally {
    if (previousNodeEnv === undefined) delete process.env.NODE_ENV;
    else process.env.NODE_ENV = previousNodeEnv;
  }
});

test("login screens gate the demo password through showDemoLoginHints", () => {
  for (const rel of ["app/login/page.tsx", "app/member/login/page.tsx"]) {
    const text = readFileSync(join(webRoot, rel), "utf8");
    assert.equal(text.includes("changeme"), false, rel);
    assert.equal(text.includes("showDemoLoginHints"), true, rel);
  }
  for (const rel of ["app/login/login-form.tsx", "app/member/login/login-form.tsx"]) {
    const text = readFileSync(join(webRoot, rel), "utf8");
    assert.equal(text.includes("changeme"), false, rel);
    assert.equal(text.includes("demo-login"), false, rel);
    assert.equal(text.includes("defaultPassword"), true, rel);
  }
});
