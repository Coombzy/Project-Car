import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

import { bandAt, lowestFreeBay, type BayChoice, type SpanInterval } from "./booking-calendar.ts";

const bays: BayChoice[] = [
  { id: "bay-1", name: "Bay 1", number: 1, isShop: false, status: "available" },
  { id: "bay-2", name: "Bay 2", number: 2, isShop: false, status: "available" },
];

const windowStart = "2026-06-18T14:00:00";
const windowEnd = "2026-06-18T16:00:00";

function span(status: string): SpanInterval {
  return { hoistId: "bay-1", startAt: windowStart, endAt: windowEnd, status };
}

describe("lowestFreeBay", () => {
  it("test_completed_visit_leaves_that_bay_free", () => {
    assert.equal(lowestFreeBay(bays, [span("completed")], windowStart, windowEnd)?.id, "bay-1");
    assert.equal(lowestFreeBay(bays, [span("confirmed")], windowStart, windowEnd)?.id, "bay-2");
    assert.equal(lowestFreeBay(bays, [span("pending")], windowStart, windowEnd)?.id, "bay-2");
    assert.equal(lowestFreeBay(bays, [span("active")], windowStart, windowEnd)?.id, "bay-2");
    assert.equal(lowestFreeBay(bays, [span("overdue")], windowStart, windowEnd)?.id, "bay-2");
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

describe("bandAt fallback", () => {
  it("uses peak on Friday evening and weekend before late night", () => {
    assert.equal(bandAt("2026-11-27", 16).id, "weekend_fri_eve");
    assert.equal(bandAt("2026-11-28", 18).id, "weekend_fri_eve");
    assert.equal(bandAt("2026-11-23", 18).id, "weekday_eve");
    assert.equal(bandAt("2026-11-27", 21).id, "late_night");
    assert.equal(bandAt("2026-11-28", 7).id, "late_night");
  });
});

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

describe("selection quote", () => {
  it("groups a server quote and skips a blank one", async () => {
    const { quotedSelectionLine } = await import("./booking-calendar.ts");
    assert.equal(quotedSelectionLine(null), null);
    assert.equal(quotedSelectionLine({ final_reserve_cost: "10", segments: [] }), null);
    assert.equal(
      quotedSelectionLine({
        final_reserve_cost: "450",
        fill_multiplier: "1.5",
        fill_label: "Short fill",
        segments: [
          { band_label: "Day", band_tokens: "100" },
          { band_label: "Day", band_tokens: "100" },
          { band_label: "Peak", band_tokens: "150" },
          { band_label: "Night", band_tokens: "10.25" },
          { band_label: "Night", band_tokens: "10.25" },
        ],
      }),
      "Day 100 × 2 = 200 · Peak 150 × 1 = 150 · Night 10.25 × 2 = 20.50 · Short fill · Total 450",
    );
    assert.equal(
      quotedSelectionLine({
        final_reserve_cost: "100",
        fill_multiplier: "1",
        fill_label: "Ignored",
        segments: [{ band_label: "Day", band_tokens: "100" }],
      }),
      "Day 100 × 1 = 100 · Total 100",
    );
  });

  it("sums selected hours and stops at a booked hour", async () => {
    const { selectionSummary } = await import("./booking-calendar.ts");
    const saved = [
      {
        weekday: 0,
        day_label: "Mon",
        hour: 10,
        band_id: "weekday_eve",
        label: "Eve",
        tokens_per_hour: "80",
        counts_toward_peak_cap: false,
      },
    ];
    assert.deepEqual(selectionSummary("2026-11-27", 18, 14), {
      hours: [14, 15, 16, 17],
      line: "Day 100 × 2 = 200 · Peak 150 × 2 = 300 · Total 500",
      note: null,
      total: 500,
    });
    assert.deepEqual(selectionSummary("2026-11-27", 14, 18, new Set([16])), {
      hours: [14, 15],
      line: "Day 100 × 2 = 200 · Total 200",
      note: "16:00 is booked; selection ends at 16:00",
      total: 200,
    });
    assert.deepEqual(selectionSummary("2026-11-23", 10, 10), {
      hours: [],
      line: "",
      note: null,
      total: 0,
    });
    assert.deepEqual(selectionSummary("2026-11-23", 10, 12, new Set(), saved), {
      hours: [10, 11],
      line: "Eve 80 × 1 = 80 · Day 100 × 1 = 100 · Total 180",
      note: null,
      total: 180,
    });
  });
});

describe("peak week and member balance", () => {
  const week = "2026-11-23";
  const friday = {
    status: "confirmed",
    startAt: "2026-11-27T16:00:00",
    endAt: "2026-11-27T18:00:00",
  };

  it("counts Friday peak hours, skips cancelled and Monday, and labels the balance", async () => {
    const { memberBalanceCopy, peakWeek } = await import("./booking-calendar.ts");
    const { tokensLabel } = await import("./time.ts");
    const peak = peakWeek([friday], week);
    assert.equal(peak.cap, 4);
    assert.equal(peak.used, 2);
    assert.equal(peak.remaining, 2);
    assert.equal(peak.line, "Peak hours this week: 2 used · 2 left");
    assert.equal(peakWeek([{ ...friday, status: "cancelled" }], week).used, 0);
    const monday = { status: "confirmed", startAt: "2026-11-23T16:00:00", endAt: "2026-11-23T18:00:00" };
    assert.equal(peakWeek([monday], week).used, 0);
    const saved = { hours: [], peakCapHours: 2 };
    const capped = peakWeek([friday], week, saved);
    assert.equal(capped.remaining, 0);
    const copy = memberBalanceCopy("10.5", "1.25", [friday], week, saved);
    assert.equal(copy.allowance, tokensLabel(10.5));
    assert.equal(copy.purchased, tokensLabel(1.25));
    assert.equal(copy.total, tokensLabel(11.75));
    assert.equal(copy.peak, capped.line);
  });
});
