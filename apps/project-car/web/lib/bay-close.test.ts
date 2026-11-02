import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

const webRoot = join(dirname(fileURLToPath(import.meta.url)), "..");
const page = readFileSync(join(webRoot, "app/hoists/page.tsx"), "utf8");
const actions = readFileSync(join(webRoot, "app/hoists/actions.ts"), "utf8");

describe("owner bay close", () => {
  it("asks for a reason and refunds future bookings when the bay closes", () => {
    assert.match(page, /Reason/);
    assert.match(page, /refund/i);
    assert.match(actions, /cancel_bookings:\s*true/);
    assert.match(actions, /maintenance/);
    assert.match(actions, /locked/);
    assert.match(actions, /reason/);
  });
});
