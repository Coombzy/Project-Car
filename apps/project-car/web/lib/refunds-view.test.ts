import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

import { refundRows } from "./refunds-view.ts";

const web = join(dirname(fileURLToPath(import.meta.url)), "..");
const src = (rel: string) => readFileSync(join(web, rel), "utf8");

describe("refundRows", () => {
  it("keeps API order and drops rows without id", () => {
    const rows = refundRows([
      { id: "new", booking_id: "b2", status: "pending", created_by_kind: "ai", created_by_id: "a" },
      null,
      "bad",
      ["nope"],
      { status: "pending" },
      { id: "" },
      { id: 1 },
      { id: "old", booking_id: "b1", status: "pending", created_by_kind: "owner", created_by_id: "o" },
    ]);
    assert.deepEqual(
      rows.map((row) => [row.id, row.booking_id, row.status, row.created_by_kind, row.created_by_id]),
      [
        ["new", "b2", "pending", "ai", "a"],
        ["old", "b1", "pending", "owner", "o"],
      ],
    );
    assert.deepEqual(refundRows(null), []);
  });

  it("does not keep a non-string booking_id", () => {
    const rows = refundRows([
      { id: "r1", booking_id: { raw: "b1" }, status: "pending", created_by_kind: "owner", created_by_id: "o" },
      { id: "n", booking_id: "b", status: 1, created_by_kind: "ai", created_by_id: "o" },
    ]);
    assert.ok(rows.every((row) => [row.booking_id, row.status, row.created_by_kind, row.created_by_id].every((field) => typeof field === "string")));
  });

  it("builds accept paths with pathSegment, and the page / shell / actions call them", () => {
    const api = src("lib/refunds-api.ts");
    const page = src("app/refund-requests/page.tsx");
    const actions = src("app/refund-requests/actions.ts");
    const shell = src("components/owner-shell.tsx");
    const has = (file: string, parts: string[]) => { for (const piece of parts) assert.ok(file.includes(piece), piece); };
    has(api, ['import { shopJson } from "./shop-api"', 'import { pathSegment } from "./shop-path"', 'shopJson<RefundRequestRow[]>("/refund-requests", "Could not load refund requests.")', "`/refund-requests/${pathSegment(id)}/accept`", 'method: "POST"']);
    assert.equal(api.includes("${id}"), false);
    has(page, ['current="refund-requests"', "getMe(", "handlePageError", "listRefundRequests(", "refundRows(", "No pending refund requests.", "Accept", "booking_id", "force-dynamic", 'type="hidden" name="id"']);
    assert.equal(page.includes('name="decision"'), false);
    has(actions, ["acceptRefundRequest(", 'revalidatePath("/refund-requests")', "/refund-requests?notice=", "/refund-requests?error=", "ShopApiError"]);
    assert.match(shell, /label: "Payments" \},\s*\{ href: "\/refund-requests", current: "refund-requests", label: "Refunds" \}/);
  });
});
