import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");

// AUD-040 part 2. Kept apart from page-titles.test.ts so #352 can merge on its own.
const pages: Record<string, string> = {
  "app/login/page.tsx": "Sign in",
  "app/member/login/page.tsx": "Sign in to your bay",
};

describe("AUD-040 login titles", () => {
  it("test_login_pages_export_a_title", () => {
    for (const [path, title] of Object.entries(pages)) {
      const source = readFileSync(join(root, path), "utf8");
      assert.equal(source.includes(`title: "${title}"`), true, path);
    }
  });
});
