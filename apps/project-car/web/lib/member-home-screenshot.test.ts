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

    // member-home.png is the shot pages.spec.ts compares. The next-visit files
    // are not that oracle, so they must not sit beside it as a second baseline.
    for (const width of ["390", "768", "1440"]) {
      assert.equal(
        existsSync(join(visual, "screenshots", width, "member-home-next-visit.png")),
        false,
        `${width}/member-home-next-visit.png is not the visual check; member-home.png is`,
      );
    }
  });

  it("test_next_visit_card_sits_under_the_metrics_in_the_member_home_shot", () => {
    // 768×1024 and 1440×900 include the metrics and the block directly under them.
    // That is the Next visit slot, so member-home.png shows the card.
    // 390×844 ends inside the metrics; the same slot is still directly under them.
    const page = readFileSync(pagePath, "utf8");
    const metricsAt = page.indexOf('className="metrics"');
    const cardAt = page.indexOf("<NextVisitCard");
    const bookAt = page.indexOf("Book a customer bay");
    const todoAt = page.indexOf("<TodoPanel");
    const openAt = page.indexOf("<h2>Open bookings</h2>");
    assert.ok(metricsAt !== -1, "member home must still render the metrics");
    assert.ok(cardAt !== -1, "member home must render the Next visit card");
    assert.ok(bookAt !== -1, "member home must still link to the schedule");
    assert.ok(todoAt !== -1, "member home must still render the to-do panel");
    assert.ok(openAt !== -1, "member home must still render open bookings");
    assert.ok(cardAt > metricsAt, "Next visit must sit under the metrics");
    assert.ok(
      cardAt < bookAt,
      "Next visit must sit directly under the metrics, above the schedule link",
    );
    assert.ok(
      cardAt < todoAt,
      "Next visit must sit above the to-do panel so the 768 and 1440 member-home shots include it",
    );
    assert.ok(cardAt < openAt, "Next visit stays above the open-bookings table");
    const tag = page.slice(cardAt, page.indexOf("/>", cardAt) + 2);
    assert.match(tag, /bookings=\{me\.bookings\}/, "the card still uses the bookings the page already loaded");
    assert.match(tag, /now=\{shopClock\(\)\}/, "the card still uses the shop clock the page already has");
    assert.equal((page.match(/<NextVisitCard\b/g) ?? []).length, 1);
  });
});
