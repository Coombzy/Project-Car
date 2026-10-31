import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

const webRoot = join(dirname(fileURLToPath(import.meta.url)), "..");
const card = readFileSync(join(webRoot, "components/owner-booking-card.tsx"), "utf8");

describe("owner check-out", () => {
  it("finishes an overdue visit and says extra hours are charged", () => {
    assert.match(card, /status === "overdue"/);
    assert.match(card, /Time past the booked end is charged by the hour/);
    assert.equal(card.includes("unused_tokens"), false);
    assert.equal(card.includes("Unused"), false);
  });
});
