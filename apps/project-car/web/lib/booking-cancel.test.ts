import assert from "node:assert/strict";

// Path-gate probe: a web source edit runs pytest, the web job, and the visual job.
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

const webRoot = join(dirname(fileURLToPath(import.meta.url)), "..");
const ownerPath = join(webRoot, "components/owner-booking-card.tsx");
const memberPath = join(webRoot, "components/member-booking-card.tsx");

function cancelGuards(source: string, action: string): string[] {
  const needle = `action={${action}}`;
  const guards: string[] = [];
  let from = 0;
  while (from < source.length) {
    const at = source.indexOf(needle, from);
    if (at === -1) {
      break;
    }
    const question = source.lastIndexOf("?", at);
    const open = source.lastIndexOf("{", question);
    assert.ok(question > open && open !== -1, `cancel form has no condition before ${action}`);
    guards.push(source.slice(open + 1, question).trim());
    from = at + needle.length;
  }
  assert.ok(guards.length > 0, `no ${action} form`);
  return guards;
}

function activeBranch(source: string): string {
  const marker = 'booking.status === "active" || booking.status === "overdue"';
  const at = source.indexOf(marker);
  assert.notEqual(at, -1, "owner card has no active branch");
  const end = source.indexOf(") : null}", at);
  assert.notEqual(end, -1, "owner active branch is unclosed");
  return source.slice(at, end);
}

describe("booking cancel on an active visit", () => {
  it("test_active_cards_do_not_offer_cancel", () => {
    const owner = readFileSync(ownerPath, "utf8");
    const member = readFileSync(memberPath, "utf8");
    const offer = readFileSync(join(webRoot, "lib/booking-calendar.ts"), "utf8");
    const ownerGuards = cancelGuards(owner, "cancelBookingAction");
    const memberGuards = cancelGuards(member, "memberCancelBookingAction");

    assert.equal(ownerGuards.length, 1, "owner card should have one cancel form");
    assert.equal(memberGuards.length, 1, "member card should have one cancel form");
    for (const guard of [...ownerGuards, ...memberGuards]) {
      assert.equal(
        guard.includes('=== "active"'),
        false,
        `cancel is offered on an active visit: ${guard}`,
      );
    }

    const ownerGuard = ownerGuards[0];
    assert.equal(ownerGuard.includes('=== "pending"'), true, "owner cancel must stay on pending");
    assert.equal(ownerGuard.includes('=== "confirmed"'), true, "owner cancel must stay on confirmed");
    assert.equal(memberGuards[0].includes("cancel?.visible"), true, "member cancel follows the cancel offer");
    assert.match(
      offer,
      /status === "active"[\s\S]*return hidden/,
      "an active visit hides the member cancel offer",
    );

    const active = activeBranch(owner);
    assert.match(active, /action=\{completeBookingAction\}/);
    assert.match(active, />\s*Finish visit\s*</);
    assert.doesNotMatch(active, /Cancel/);
    assert.doesNotMatch(active, /cancelBookingAction/);
  });
});
