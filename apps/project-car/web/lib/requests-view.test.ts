import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";
import { groupRequests } from "./requests-view.ts";

const web = join(dirname(fileURLToPath(import.meta.url)), "..");

describe("groupRequests", () => {
  it("groups three kinds, oldest shop hoist first, and drops unknown keys", () => {
    const groups = groupRequests({
      refunds: [{ id: "no" }],
      tool_crib: [{ id: "t2", created_at: "2026-06-02" }, { id: "t1", created_at: "2026-06-01" }],
      parts: [{ id: "p2", created_at: "2026-05-02" }, { id: "p1", created_at: "2026-05-01" }],
      shop_hoist: [{ id: "new", created_at: "2026-04-02T00:00:00Z" }, { id: "old", created_at: "2026-04-01T00:00:00Z" }],
    });
    assert.deepEqual(groups.map((group) => [group.kind, group.label, group.rows.map((row) => row.id)]), [
      ["shop_hoist", "Shop hoist", ["old", "new"]],
      ["parts", "Parts", ["p2", "p1"]],
      ["tool_crib", "Tool crib", ["t2", "t1"]],
    ]);
  });

  it("omits empty groups", () => {
    assert.deepEqual(groupRequests({ shop_hoist: [], parts: [{ id: "p" }], tool_crib: [] }).map((group) => group.kind), ["parts"]);
  });

  it("builds decide paths with pathSegment, not a bare id", () => {
    const api = readFileSync(join(web, "lib/requests-api.ts"), "utf8");
    const page = readFileSync(join(web, "app/requests/page.tsx"), "utf8");
    const actions = readFileSync(join(web, "app/requests/actions.ts"), "utf8");
    assert.equal(/\$\{(?:id|name|request_id)\}/.test(api), false);
    for (const needle of ['shop_hoist: "/shop-hoist-requests"', 'parts: "/staff/parts-requests"', 'tool_crib: "/tool-crib-exceptions"', "${pathSegment(id)}"]) assert.equal(api.includes(needle), true, needle);
    for (const needle of ["listStaffRequests(", "getMe(", "handlePageError", 'current="requests"', "No pending requests.", "member_name", "member_id", "hoist_name", "sku", "tool_code", "Approve", "Deny"]) assert.equal(page.includes(needle), true, needle);
    for (const needle of ["decideRequest(", 'revalidatePath("/requests")', "/requests?notice=", "ShopApiError", "/requests?error="]) assert.equal(actions.includes(needle), true, needle);
    assert.match(page, /type="hidden" name="decision" value="approve"/);
    assert.match(page, /type="hidden" name="decision" value="deny"/);
    assert.doesNotMatch(page, /<button[^>]*name="decision"/);
  });
});
