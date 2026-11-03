import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

const webRoot = join(dirname(fileURLToPath(import.meta.url)), "..");
const page = readFileSync(join(webRoot, "app/members/[id]/page.tsx"), "utf8");
const actions = readFileSync(join(webRoot, "app/members/actions.ts"), "utf8");
const shopApi = readFileSync(join(webRoot, "lib/shop-api.ts"), "utf8");

function functionSource(source: string, name: string): string {
  const marker = `export async function ${name}`;
  const start = source.indexOf(marker);
  assert.notEqual(start, -1, `${name} is missing`);
  const next = source.indexOf("\nexport async function ", start + marker.length);
  return source.slice(start, next === -1 ? source.length : next);
}

describe("manual token change", () => {
  it("requires a reason and sends it with the adjustment", () => {
    const formStart = page.indexOf("action={adjustTokensAction}");
    const form = page.slice(page.lastIndexOf("<form", formStart), page.indexOf("</form>", formStart));
    assert.match(form, /name="reason"/);
    assert.match(form, /required/);
    assert.match(actions, /formData\.get\("reason"\)/);
    assert.match(actions, /reason/);
  });

  it("posts the typed reason as the ledger note", () => {
    const adjust = functionSource(shopApi, "adjustMemberTokens");
    const posted = adjust.match(/JSON\.stringify\((\{[\s\S]*?\})\)/);
    assert.ok(posted, "adjustMemberTokens must post a JSON body");
    const literal = posted[1];
    assert.match(literal, /\bamount\b/);
    assert.match(
      literal,
      /note\s*:\s*reason\b/,
      "the ledger note must be the typed reason, not a separate unread field",
    );
  });
});
