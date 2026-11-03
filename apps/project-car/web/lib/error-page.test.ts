import assert from "node:assert/strict";
import { existsSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

const webRoot = join(dirname(fileURLToPath(import.meta.url)), "..");

function readSource(relativePath: string): string {
  const abs = join(webRoot, relativePath);
  assert.equal(existsSync(abs), true, `${relativePath} is missing`);
  return readFileSync(abs, "utf8");
}

describe("shop error page", () => {
  it("test_error_page_uses_the_shop_shell", () => {
    const errorPage = readSource("app/error.tsx");

    assert.equal(
      errorPage.trimStart().startsWith('"use client"'),
      true,
      'error.tsx must start with "use client"',
    );
    assert.match(errorPage, /Something went wrong\. Try again\./);
    assert.match(errorPage, /OwnerShell/);
    assert.match(errorPage, /reset:\s*\(\)\s*=>\s*void/);
    assert.match(
      errorPage,
      /<button type="button" onClick=\{\(\) => reset\(\)\}>Try again<\/button>/,
    );
    assert.equal(errorPage.includes("error.message"), false, "error.tsx renders error.message");
    assert.equal(errorPage.includes("error.stack"), false, "error.tsx renders error.stack");
    assert.doesNotMatch(errorPage, /error\??\.(message|stack|digest)/);
    assert.doesNotMatch(errorPage, /\{error\}/);
  });
});
