import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { afterEach, test } from "node:test";
import { join } from "node:path";

import { showDemoLoginHints } from "./demo-login.ts";

const webRoot = join(import.meta.dirname, "..");

const forms = [
  ["app/login/login-form.tsx", "owner@projectcar.ca"],
  ["app/member/login/login-form.tsx", "ada.reyes@example.com"],
] as const;

function read(rel: string): string {
  return readFileSync(join(webRoot, rel), "utf8");
}

afterEach(() => {
  delete process.env.SHOP_DEMO_LOGIN_HINTS;
});

test("login forms gate demo email and password defaults on showDemoLoginHints", () => {
  for (const [rel, email] of forms) {
    const text = read(rel);
    assert.equal(
      text.includes(`defaultValue="${email}"`),
      false,
      `${rel} has an unguarded demo email defaultValue`,
    );
    assert.equal(
      text.includes(`defaultValue='${email}'`),
      false,
      `${rel} has an unguarded demo email defaultValue`,
    );
    assert.equal(text.includes("showDemoLoginHints"), true, `${rel} does not reference showDemoLoginHints`);
    assert.match(text, /import \{ showDemoLoginHints \} from "(\.\.\/)+lib\/login-hints"/, rel);
    assert.match(
      text,
      new RegExp(`defaultValue=\\{hints \\? "${email.replaceAll(".", "\\.")}" : ""\\}`),
      `${rel} email default`,
    );
    assert.match(
      text,
      /defaultValue=\{hints \? \(defaultPassword \?\? ""\) : ""\}/,
      `${rel} password default`,
    );
    assert.equal(text.includes("defaultValue={defaultPassword ?? \"\"}"), false, rel);
  }

  const hints = read("lib/login-hints.ts");
  assert.match(hints, /export \{ showDemoLoginHints \} from "\.\/demo-login"/);

  delete process.env.SHOP_DEMO_LOGIN_HINTS;
  assert.equal(showDemoLoginHints(), false);
  process.env.SHOP_DEMO_LOGIN_HINTS = "true";
  assert.equal(showDemoLoginHints(), true);
});
