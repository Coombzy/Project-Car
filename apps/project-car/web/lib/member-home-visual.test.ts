import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

const webRoot = join(dirname(fileURLToPath(import.meta.url)), "..");
const visual = join(webRoot, "visual");

const NEXT_VISIT_SHOT: Record<string, string> = {
  "768": "4f600f5ec4328f34fc2c08f9b940c7bbef21309f7c663e04edcf62d411e33771",
  "1440": "5808d86939ca6a3a5168d22dfe22b4bd9c5448fa4d41228e7ff09950bb66fb62",
};

describe("member home visual oracle", () => {
  it("test_visual_build_does_not_overwrite_member_home_or_kill_shop_ports", () => {
    const build = readFileSync(join(visual, "build-web.sh"), "utf8");
    assert.equal(build.includes("free_visual_ports"), false, "visual build must not signal shop ports");
    assert.equal(build.includes("playwright install"), false, "visual build must not install browsers");
    assert.equal(
      build.includes("member-home-ref"),
      false,
      "visual build must not decode a hidden member-home reference",
    );
    assert.equal(build.includes("base64 -d"), false, "visual build must not rewrite screenshot baselines");
    assert.match(build, /npm run build/, "visual build must still build the shop web");
    assert.equal(existsSync(join(visual, "member-home-ref", "768.b64")), false);
    assert.equal(existsSync(join(visual, "member-home-ref", "1440.b64")), false);

    const spec = readFileSync(join(visual, "pages.spec.ts"), "utf8");
    assert.match(spec, /toHaveScreenshot\(/, "member pages must still be screenshot");
    assert.match(spec, /MAX_LAYOUT_SHIFT = 0\.1/);
    assert.equal(spec.includes("test.skip"), false);
    assert.match(
      spec,
      /name === "member-home"[\s\S]*project === "768" \|\| project === "1440"[\s\S]*member-home-next-visit/,
      "768 and 1440 member-home must compare to the reference that includes the Next visit card",
    );

    const config = readFileSync(join(webRoot, "playwright.config.ts"), "utf8");
    assert.match(config, /maxDiffPixelRatio: 0\.01/);

    for (const [width, hash] of Object.entries(NEXT_VISIT_SHOT)) {
      const path = join(visual, "screenshots", width, "member-home-next-visit.png");
      assert.equal(existsSync(path), true, `${width} member-home reference must include the Next visit card`);
      const digest = createHash("sha256").update(readFileSync(path)).digest("hex");
      assert.equal(digest, hash, `${width} member-home-next-visit.png`);
    }
  });
});
