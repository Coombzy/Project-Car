import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");

// AUD-040 part 1. Login pages are #337 and are not in this list.
const pages: Record<string, string> = {
  "app/page.tsx": "title: { absolute: \"Shop dashboard · Project Car\" }",
  "app/schedule/page.tsx": "Schedule",
  "app/chat/page.tsx": "Shop chat",
  "app/chat/[id]/page.tsx": "Shop chat",
  "app/members/page.tsx": "Members",
  "app/members/[id]/page.tsx": "Member",
  "app/parts/page.tsx": "Parts",
  "app/tools/page.tsx": "Tools",
  "app/jobs/page.tsx": "Job board",
  "app/cameras/page.tsx": "Cameras",
  "app/hoists/page.tsx": "Hoists",
  "app/payments/page.tsx": "Payments",
  "app/tiers/page.tsx": "Tiers",
  "app/fill/page.tsx": "Fill the gaps",
  "app/waitlist/page.tsx": "Waitlist",
  "app/signup/page.tsx": "Sign up",
  "app/member/page.tsx": "Your shop",
  "app/member/profile/page.tsx": "Profile",
  "app/member/schedule/page.tsx": "Schedule",
  "app/member/chat/page.tsx": "Shop chat",
  "app/member/chat/[id]/page.tsx": "Shop chat",
  "app/member/parts/page.tsx": "Parts requests",
  "app/member/jobs/page.tsx": "Job board",
  "app/member/cameras/page.tsx": "Shop camera",
};

describe("AUD-040 page titles", () => {
  it("test_root_layout_exports_a_title_template", () => {
    const layout = readFileSync(join(root, "app/layout.tsx"), "utf8");
    assert.match(layout, /default:\s*"Project Car · Shop OS"/);
    assert.match(layout, /template:\s*"%s · Project Car"/);
    assert.match(
      layout,
      /description:\s*"Bay time, parts, and jobs for your car\. The shop is not open\."/,
    );
    assert.doesNotMatch(layout, /ops\.projectcar\.ca|app\.projectcar\.ca|temporary park/);
  });

  it("test_listed_pages_export_a_title", () => {
    for (const [path, title] of Object.entries(pages)) {
      const source = readFileSync(join(root, path), "utf8");
      const needle = path === "app/page.tsx" ? title : `title: "${title}"`;
      assert.equal(source.includes(needle), true, path);
    }
  });
});
