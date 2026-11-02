import assert from "node:assert/strict";
import { existsSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

import { showDemoLoginHints } from "./demo-login.ts";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");

const CLIENT_LOGIN_FORMS = ["app/login/login-form.tsx", "app/member/login/login-form.tsx"];

function resolveRelative(fromFile: string, spec: string): string | null {
  const base = join(root, dirname(fromFile), spec);
  const candidates = [
    base,
    `${base}.ts`,
    `${base}.tsx`,
    join(base, "index.ts"),
    join(base, "index.tsx"),
  ];
  for (const candidate of candidates) {
    if (existsSync(candidate)) {
      return candidate.slice(root.length + 1);
    }
  }
  return null;
}

/** Files a client login form pulls in. The demo password must not be among them. */
function clientModuleGraph(entry: string): string[] {
  const seen = new Set<string>();
  const queue = [entry];
  while (queue.length > 0) {
    const file = queue.pop();
    if (file === undefined || seen.has(file)) {
      continue;
    }
    seen.add(file);
    const text = readFileSync(join(root, file), "utf8");
    const pattern = /from\s+["'](\.[^"']+)["']/g;
    for (const match of text.matchAll(pattern)) {
      const spec = match[1];
      if (spec === undefined) {
        continue;
      }
      const resolved = resolveRelative(file, spec);
      if (resolved !== null) {
        queue.push(resolved);
      }
    }
  }
  return [...seen];
}

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

it("server login pages pass the demo password only when hints are on", () => {
  const pages = [
    ["app/login/page.tsx", "demoOwnerPassword"],
    ["app/member/login/page.tsx", "demoMemberPassword"],
  ] as const;
  for (const [file, passwordFn] of pages) {
    const text = readFileSync(join(root, file), "utf8");
    assert.match(text, /showDemoLoginHints/);
    assert.match(text, new RegExp(`hints \\? ${passwordFn}\\(\\)`));
    assert.equal(text.includes("changeme"), false, file);
  }
});

it("client login forms do not import the demo password module", () => {
  for (const file of CLIENT_LOGIN_FORMS) {
    const text = readFileSync(join(root, file), "utf8");
    assert.equal(text.includes("demo-login"), false, file);
    assert.equal(text.includes("showDemoLoginHints"), false, file);
    assert.equal(text.includes("changeme"), false, file);
    assert.match(text, /defaultPassword/);
    for (const imported of clientModuleGraph(file)) {
      const importedText = readFileSync(join(root, imported), "utf8");
      assert.equal(importedText.includes("changeme"), false, `${file} -> ${imported}`);
    }
  }
});
