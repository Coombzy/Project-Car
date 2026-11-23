import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

import { lowestFreeBay, type BayChoice, type SpanInterval } from "./booking-calendar.ts";

const bays: BayChoice[] = [
  { id: "bay-1", name: "Bay 1", number: 1, isShop: false, status: "available" },
  { id: "bay-2", name: "Bay 2", number: 2, isShop: false, status: "available" },
];

const start = "2026-06-18T14:00:00";
const end = "2026-06-18T16:00:00";

function span(status: string): SpanInterval {
  return { hoistId: "bay-1", startAt: start, endAt: end, status };
}

describe("lowestFreeBay", () => {
  it("test_completed_visit_leaves_that_bay_free", () => {
    assert.equal(lowestFreeBay(bays, [span("completed")], start, end)?.id, "bay-1");
    assert.equal(lowestFreeBay(bays, [span("confirmed")], start, end)?.id, "bay-2");
    assert.equal(lowestFreeBay(bays, [span("pending")], start, end)?.id, "bay-2");
    assert.equal(lowestFreeBay(bays, [span("active")], start, end)?.id, "bay-2");
    assert.equal(lowestFreeBay(bays, [span("overdue")], start, end)?.id, "bay-2");
  });
});

const webRoot = join(dirname(fileURLToPath(import.meta.url)), "..");
const pagePath = join(webRoot, "app/member/schedule/page.tsx");
const cardPath = join(webRoot, "components/member-booking-card.tsx");
const homePath = join(webRoot, "app/member/page.tsx");
const wordsPath = join(webRoot, "lib/booking-words.ts");
const calendarPath = join(webRoot, "lib/booking-calendar.ts");

const YOUR_BOOKINGS = ["active", "confirmed", "overdue", "pending"];

function statusesIn(source: string): string[] {
  return [...source.matchAll(/booking\.status === "([a-z_]+)"/g)].map((match) => match[1]).sort();
}

describe("Your bookings", () => {
  it("lists a checked-in visit under Your bookings", async () => {
    const page = readFileSync(pagePath, "utf8");
    const card = readFileSync(cardPath, "utf8");
    const problems: string[] = [];

    const start = page.indexOf("const yours = me.bookings.filter(");
    if (start === -1) {
      problems.push("no me.bookings filter");
    } else {
      const filter = page.slice(start, page.indexOf(");", start));
      const statuses = statusesIn(filter);
      if (JSON.stringify(statuses) !== JSON.stringify(YOUR_BOOKINGS)) {
        problems.push(`filter is ${statuses.join(", ") || "empty"}`);
      }
      if (filter.includes("no_show")) {
        problems.push("filter includes no_show");
      }
    }

    if (!page.includes("Your bookings")) {
      problems.push('page has no "Your bookings" heading');
    }
    const zeroAt = page.indexOf("yours.length === 0");
    const emptyAt = page.indexOf("No upcoming bookings.");
    if (zeroAt === -1 || emptyAt === -1 || emptyAt < zeroAt) {
      problems.push('checked-in visit can still show "No upcoming bookings."');
    }

    let label = "";
    let overdueLabel = "";
    let activeVisible: boolean | null = null;
    let overdueVisible: boolean | null = null;
    try {
      const words = await import("./booking-words.ts");
      const calendar = await import("./booking-calendar.ts");
      label = words.bookingStatusLabel("active");
      overdueLabel = words.bookingStatusLabel("overdue");
      const now = new Date("2026-11-05T22:00:00.000Z");
      activeVisible = calendar.memberCancelOffer(
        { status: "active", startAt: "2026-11-06T22:00:00", reservedTokens: "100" },
        now,
      ).visible;
      overdueVisible = calendar.memberCancelOffer(
        { status: "overdue", startAt: "2026-11-04T16:00:00", reservedTokens: "100" },
        now,
      ).visible;
    } catch {
      problems.push("no memberCancelOffer");
    }

    if (!card.includes("memberCancelOffer") && !problems.includes("no memberCancelOffer")) {
      problems.push("no memberCancelOffer");
    }
    if (!card.includes("bookingStatusLabel")) {
      problems.push("card does not label the visit");
    }
    if (label !== "In the bay") {
      problems.push('an active visit is not labelled "In the bay"');
    }
    if (overdueLabel !== "Late") {
      problems.push('overdue is not labelled "Late"');
    }
    if (activeVisible !== false) {
      problems.push("active visit offers cancel");
    }
    if (overdueVisible !== false) {
      problems.push("overdue visit offers cancel");
    }

    assert.deepEqual(problems, [], problems.join("; "));
  });

  it("refunds the whole reserve before the start and hides cancel after it", async () => {
    const { memberCancelOffer } = await import("./booking-calendar.ts");
    // 22:00Z is 16:00 America/Regina. A naive shop time is that zone (UTC−6).
    const now = new Date("2026-11-05T22:00:00.000Z");

    const soon = memberCancelOffer(
      { status: "confirmed", startAt: "2026-11-05T17:00:00", reservedTokens: "337.51" },
      now,
    );
    assert.equal(soon.visible, true);
    assert.equal(soon.refund, 337.51);
    assert.equal(soon.kept, 0);
    assert.equal(soon.label, "Cancel");

    const early = memberCancelOffer(
      { status: "pending", startAt: "2026-11-07T16:00:00", reservedTokens: "200" },
      now,
    );
    assert.equal(early.visible, true);
    assert.equal(early.refund, 200);
    assert.equal(early.kept, 0);

    const started = memberCancelOffer(
      { status: "confirmed", startAt: "2026-11-05T15:00:00", reservedTokens: "100" },
      now,
    );
    assert.equal(started.visible, false);

    for (const status of ["completed", "cancelled", "active", "overdue"]) {
      const offer = memberCancelOffer(
        { status, startAt: "2026-11-07T16:00:00", reservedTokens: "80" },
        now,
      );
      assert.equal(offer.visible, false, status);
    }
  });

  it("names the other statuses and does not add no_show", async () => {
    const { bookingStatusLabel } = await import("./booking-words.ts");
    assert.equal(bookingStatusLabel("pending"), "Waiting");
    assert.equal(bookingStatusLabel("confirmed"), "Booked");
    assert.equal(bookingStatusLabel("completed"), "Finished");
    assert.equal(bookingStatusLabel("cancelled"), "Cancelled");

    const words = readFileSync(wordsPath, "utf8");
    const calendar = readFileSync(calendarPath, "utf8");
    const page = readFileSync(pagePath, "utf8");
    assert.equal(words.includes("no_show"), false);
    assert.equal(calendar.includes("no_show"), false);
    assert.equal(page.includes("no_show"), false);
  });

  it("keeps the home list on pending, confirmed, and active", () => {
    const home = readFileSync(homePath, "utf8");
    const start = home.indexOf("const open = me.bookings.filter(");
    assert.notEqual(start, -1, "home bookings filter is missing");
    const filter = home.slice(start, home.indexOf(");", start));
    assert.deepEqual(statusesIn(filter), ["active", "confirmed", "pending"]);
  });
});
