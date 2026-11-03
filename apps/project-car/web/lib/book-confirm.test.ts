import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

const actionsPath = join(dirname(fileURLToPath(import.meta.url)), "../app/member/schedule/actions.ts");

function functionSource(source: string, name: string): string {
  const marker = `export async function ${name}`;
  const start = source.indexOf(marker);
  assert.notEqual(start, -1, `${name} is missing`);
  const next = source.indexOf("\nexport async function ", start + marker.length);
  return source.slice(start, next === -1 ? source.length : next);
}

describe("member book confirms the created visit", () => {
  it("confirms the created row when it is not already confirmed", () => {
    const book = functionSource(readFileSync(actionsPath, "utf8"), "memberCreateBookingAction");
    const createAt = book.indexOf("const created = await createMemberBooking(");
    const guardAt = book.indexOf('created.status !== "confirmed"');
    const confirmAt = book.indexOf("await confirmMemberBooking(created.id)");
    const catchAt = book.indexOf("} catch");
    assert.notEqual(createAt, -1, "Book must keep the created row");
    assert.notEqual(guardAt, -1, "Book must skip confirm when the row is already confirmed");
    assert.notEqual(confirmAt, -1, "Book must confirm the created row");
    assert.ok(createAt < guardAt && guardAt < confirmAt && confirmAt < catchAt, book);
  });
});
