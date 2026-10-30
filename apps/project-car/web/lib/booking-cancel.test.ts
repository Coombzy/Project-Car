import assert from "node:assert/strict";
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
  const marker = 'booking.status === "active" ?';
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
    const ownerGuards = cancelGuards(owner, "cancelBookingAction");
    const memberGuards = cancelGuards(member, "memberCancelBookingAction");

    assert.equal(ownerGuards.length, 1, "owner card should have one cancel form");
    assert.equal(memberGuards.length, 2, "member card should cancel pending and confirmed separately");
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
    assert.equal(
      memberGuards.some((guard) => guard.includes('=== "pending"')),
      true,
      "member cancel must stay on pending",
    );
    assert.equal(
      memberGuards.some((guard) => guard.includes('=== "confirmed"') && !guard.includes('=== "active"')),
      true,
      "member cancel must stay on confirmed",
    );

    const active = activeBranch(owner);
    assert.match(active, /action=\{completeBookingAction\}/);
    assert.match(active, />\s*Complete\s*</);
    assert.doesNotMatch(active, /Cancel/);
    assert.doesNotMatch(active, /cancelBookingAction/);
  });
});

describe("seeded active visit on the week grid", () => {
  it("test_week_schedule_spec_checks_the_seeded_active_card", () => {
    const specPath = join(webRoot, "visual/pages.spec.ts");
    const spec = readFileSync(specPath, "utf8");
    const name = 'test("test_active_visit_hides_cancel_keeps_complete"';
    const at = spec.indexOf(name);
    assert.notEqual(
      at,
      -1,
      "visual/pages.spec.ts does not check the seeded active card on the week grid",
    );
    const body = spec.slice(at);
    assert.match(body, /\/schedule\?view=week/);
    assert.match(body, /\/member\/schedule\?view=week/);
    assert.match(body, /Riley Park/);
    assert.match(body, /riley\.park@example\.com/);
    assert.match(body, /Ada Reyes/);
    assert.match(body, /hasText: "Cancel"/);
    assert.match(body, /hasText: "Complete"/);
    assert.match(body, /toHaveCount\(0\)/);
    assert.match(body, /toHaveCount\(1\)/);
    assert.match(body, /\.pill-confirmed/);
    assert.doesNotMatch(body, /toHaveScreenshot/);
    assert.doesNotMatch(body, /maxDiffPixelRatio/);
  });
});
