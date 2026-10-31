import assert from "node:assert/strict";
import { existsSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

const webRoot = join(dirname(fileURLToPath(import.meta.url)), "..");
const visual = join(webRoot, "visual");
const pagePath = join(webRoot, "app/member/page.tsx");

describe("member home screenshot oracle", () => {
  it("test_member_home_screenshot_stays_on_member_home_png", () => {
    const spec = readFileSync(join(visual, "pages.spec.ts"), "utf8");
    assert.equal(spec.includes("memberHomeShot"), false, "do not swap the member-home snapshot name");
    assert.equal(
      spec.includes("member-home-next-visit"),
      false,
      "do not point member-home at a new baseline",
    );
    assert.match(
      spec,
      /await expect\(page\)\.toHaveScreenshot\(`\$\{name\}\.png`\);/,
      "member-home must compare to member-home.png at 390, 768, and 1440",
    );
    assert.match(spec, /toHaveScreenshot\(/, "member pages must still be screenshot");
    assert.match(spec, /MAX_LAYOUT_SHIFT = 0\.1/);
    assert.equal(spec.includes("test.skip"), false);
    assert.equal(spec.includes("maxDiffPixelRatio"), false, "the 1% cap stays in playwright.config.ts");

    const config = readFileSync(join(webRoot, "playwright.config.ts"), "utf8");
    assert.match(config, /maxDiffPixelRatio: 0\.01/);

    assert.equal(
      existsSync(join(webRoot, "lib", "member-home-visual.test.ts")),
      false,
      "do not keep a test that requires a member-home-next-visit baseline",
    );

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
  });

  it("test_next_visit_card_sits_below_the_member_home_screenshot_fold", () => {
    // 768×1024 cuts through the bay grid. 1440×900 cuts through the first to-do.
    // A card above TodoPanel is inside those folds and moves member-home.png
    // past the 1% cap (10383 px at 768, 18822 px at 1440). 390×844 already
    // ends in the metrics, so the same slot stays under that fold too.
    const page = readFileSync(pagePath, "utf8");
    const cardAt = page.indexOf("<NextVisitCard");
    const todoAt = page.indexOf("<TodoPanel");
    const openAt = page.indexOf("<h2>Open bookings</h2>");
    assert.ok(cardAt !== -1, "member home must render the Next visit card");
    assert.ok(todoAt !== -1, "member home must still render the to-do panel");
    assert.ok(openAt !== -1, "member home must still render open bookings");
    assert.ok(
      cardAt > todoAt,
      "Next visit must sit below the to-do panel so 768 and 1440 stay on member-home.png",
    );
    assert.ok(cardAt < openAt, "Next visit stays above the open-bookings table");
    const tag = page.slice(cardAt, page.indexOf("/>", cardAt) + 2);
    assert.match(tag, /bookings=\{me\.bookings\}/, "the card still uses the bookings the page already loaded");
    assert.match(tag, /now=\{shopClock\(\)\}/, "the card still uses the shop clock the page already has");
    assert.equal((page.match(/<NextVisitCard\b/g) ?? []).length, 1);
  });
});
