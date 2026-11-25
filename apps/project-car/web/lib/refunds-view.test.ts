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

  it("builds accept paths with pathSegment, and the page / shell / actions call them", () => {
    const api = src("lib/refunds-api.ts");
    const page = src("app/refund-requests/page.tsx");
    const actions = src("app/refund-requests/actions.ts");
    const shell = src("components/owner-shell.tsx");
    assert.match(api, /import \{ shopJson \} from "\.\/shop-api"/);
    assert.match(api, /import \{ pathSegment \} from "\.\/shop-path"/);
    assert.match(api, /shopJson\("\/refund-requests", "Could not load refund requests\."\)/);
    assert.match(api, /`\/refund-requests\/\$\{pathSegment\(id\)\}\/accept`/);
    assert.match(api, /method: "POST"/);
    assert.equal(api.includes("${id}"), false);
    assert.match(page, /current="refund-requests"/);
    assert.match(page, /getMe\(/);
    assert.match(page, /handlePageError/);
    assert.match(page, /listRefundRequests\(/);
    assert.match(page, /refundRows\(/);
    assert.match(page, /No pending refund requests\./);
    assert.match(page, /Accept/);
    assert.match(page, /booking_id/);
    assert.match(page, /force-dynamic/);
    assert.match(page, /type="hidden" name="id"/);
    assert.equal(page.includes('name="decision"'), false);
    assert.match(actions, /acceptRefundRequest\(/);
    assert.match(actions, /revalidatePath\("\/refund-requests"\)/);
    assert.match(actions, /\/refund-requests\?notice=/);
    assert.match(actions, /\/refund-requests\?error=/);
    assert.match(actions, /ShopApiError/);
    assert.match(shell, /label: "Payments" \},\s*\{ href: "\/refund-requests", current: "refund-requests", label: "Refunds" \}/);
  });
});
