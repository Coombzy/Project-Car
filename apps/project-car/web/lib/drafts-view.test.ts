import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

import { draftRows, type StaffDraft } from "./drafts-view.ts";
import { pathSegment } from "./shop-path.ts";

const web = join(dirname(fileURLToPath(import.meta.url)), "..");

function draft(kind: StaffDraft["kind"], extra: Partial<StaffDraft> = {}): StaffDraft {
  return { id: kind, status: "draft", body: `${kind} body`, room_id: null, ...extra, kind };
}

describe("draftRows", () => {
  it("links a chat room, not a fill draft, and keeps API order", () => {
    const room = "room/a b";
    const rows = draftRows([
      draft("chat", { id: "c", room_id: room }),
      draft("fill", { id: "f", room_id: room }),
      draft("chat", { id: "n" }),
      draft("other" as StaffDraft["kind"], { id: "x" }),
    ]);
    assert.deepEqual(
      rows.map((row) => [row.draft.id, row.roomHref, row.draft.body]),
      [
        ["c", `/chat/${pathSegment(room)}`, "chat body"],
        ["f", null, "fill body"],
        ["n", null, "chat body"],
      ],
    );
    assert.equal(rows[0]?.roomHref, `/chat/${encodeURIComponent(room)}`);
  });

  it("returns an empty list for no drafts", () => {
    assert.deepEqual(draftRows([]), []);
  });

  it("builds accept paths with pathSegment and the page calls them", () => {
    const api = readFileSync(join(web, "lib/drafts-api.ts"), "utf8");
    const page = readFileSync(join(web, "app/drafts/page.tsx"), "utf8");
    const actions = readFileSync(join(web, "app/drafts/actions.ts"), "utf8");
    assert.match(api, /listStaffDrafts/);
    assert.match(api, /\/fill\/drafts\/\$\{pathSegment\(id\)\}\/accept/);
    assert.match(api, /\/chat\/drafts\/\$\{pathSegment\(id\)\}\/accept/);
    assert.equal(api.match(/\$\{(?:id|name|job_id|draft_id)\}/g), null);
    assert.match(page, /listStaffDrafts\(/);
    assert.match(page, /getMe\(/);
    assert.match(page, /handlePageError/);
    assert.match(page, /current="fill"/);
    assert.match(page, /No pending drafts\./);
    assert.match(page, /roomHref/);
    assert.match(actions, /acceptFillDraft/);
    assert.match(actions, /acceptChatDraft/);
    assert.match(actions, /revalidatePath\("\/drafts"\)/);
    assert.match(actions, /\/drafts\?notice=/);
    assert.match(actions, /ShopApiError/);
    assert.match(actions, /\/drafts\?error=/);
  });
});
