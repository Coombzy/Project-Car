import assert from "node:assert/strict";
import { describe, it } from "node:test";

import { TIME_LABEL, bookingStatusLabel } from "./booking-words.ts";
import {
  bandAt,
  bookingErrorCopy,
  calendarViewForWidth,
  gstLine,
  lowestFreeBay,
  memberCancelOffer,
  peakWeek,
  selectionSummary,
} from "./booking-calendar.ts";

const BAYS = [
  { id: "b1", name: "Bay 1", number: 1, isShop: false, status: "available" },
  { id: "b2", name: "Bay 2", number: 2, isShop: false, status: "available" },
  { id: "b3", name: "Bay 3", number: 3, isShop: false, status: "maintenance" },
  { id: "b6", name: "Bay 6", number: 6, isShop: true, status: "available" },
];

describe("booking words", () => {
  it("labels shop time Mountain Time and a no-show in words", () => {
    assert.equal(TIME_LABEL, "Mountain Time");
    assert.equal(bookingStatusLabel("no_show"), "No-show");
    assert.equal(bookingStatusLabel("confirmed"), "Booked");
  });
});

describe("hour bands", () => {
  it("prices Thursday 15:00 as day and 17:00 as evening", () => {
    assert.equal(bandAt("2026-11-05", 15).gutter, "Day 100");
    assert.equal(bandAt("2026-11-05", 17).gutter, "Eve 125");
    assert.equal(bandAt("2026-11-05", 2).gutter, "Night 75");
    assert.equal(bandAt("2026-11-06", 17).gutter, "Peak 150");
  });
});

describe("selection", () => {
  it("sums a Thursday afternoon by the band of each hour", () => {
    // 14:00 and 15:00 are weekday day; 16:00 starts the evening band.
    assert.equal(
      selectionSummary("2026-11-05", 14, 18).line,
      "Day 100 × 2 = 200 · Eve 125 × 2 = 250 · Total 450",
    );
  });

  it("stops a range at the first booked hour", () => {
    const summary = selectionSummary("2026-11-05", 15, 19, new Set([18]));
    assert.deepEqual(summary.hours, [15, 16, 17]);
    assert.equal(summary.note, "18:00 is booked; selection ends at 18:00");
    assert.equal(summary.total, 100 + 125 + 125);
  });
});

describe("any bay", () => {
  it("picks the lowest-numbered member bay free for the whole span", () => {
    const chosen = lowestFreeBay(
      BAYS,
      [
        {
          hoistId: "b1",
          startAt: "2026-11-05T17:00:00",
          endAt: "2026-11-05T18:00:00",
          status: "confirmed",
        },
      ],
      "2026-11-05T16:00:00",
      "2026-11-05T18:00:00",
    );
    assert.equal(chosen?.id, "b2");
  });

  it("returns none when every member bay is taken or closed", () => {
    const chosen = lowestFreeBay(
      BAYS,
      [
        {
          hoistId: "b1",
          startAt: "2026-11-05T16:00:00",
          endAt: "2026-11-05T18:00:00",
          status: "confirmed",
        },
        {
          hoistId: "b2",
          startAt: "2026-11-05T16:00:00",
          endAt: "2026-11-05T18:00:00",
          status: "confirmed",
        },
      ],
      "2026-11-05T16:00:00",
      "2026-11-05T18:00:00",
    );
    assert.equal(chosen, null);
  });
});

describe("cancel, peak, gst, and the taken message", () => {
  const now = new Date("2026-11-05T22:00:00.000Z");

  it("refunds all of a cancel 24 hours ahead and half inside the window", () => {
    const early = memberCancelOffer(
      { status: "confirmed", startAt: "2026-11-06T22:00:00", reservedTokens: "200" },
      now,
    );
    assert.equal(early.visible, true);
    assert.equal(early.refund, 200);
    assert.match(early.label, /200/);

    const late = memberCancelOffer(
      { status: "confirmed", startAt: "2026-11-05T20:00:00", reservedTokens: "337.51" },
      now,
    );
    assert.equal(late.visible, true);
    assert.equal(late.kept, 168.76);
    assert.equal(late.refund, 168.75);

    const started = memberCancelOffer(
      { status: "confirmed", startAt: "2026-11-05T15:00:00", reservedTokens: "100" },
      now,
    );
    assert.equal(started.visible, false);
    assert.equal(
      memberCancelOffer(
        { status: "active", startAt: "2026-11-06T22:00:00", reservedTokens: "100" },
        now,
      ).visible,
      false,
    );
  });

  it("counts 4 peak hours a week and shows what is left", () => {
    const usage = peakWeek(
      [
        {
          status: "confirmed",
          startAt: "2026-11-06T17:00:00",
          endAt: "2026-11-06T19:00:00",
        },
        {
          status: "cancelled",
          startAt: "2026-11-07T17:00:00",
          endAt: "2026-11-07T19:00:00",
        },
      ],
      "2026-11-02",
    );
    assert.equal(usage.cap, 4);
    assert.equal(usage.used, 2);
    assert.equal(usage.remaining, 2);
    assert.match(usage.line, /2 used/);
    assert.match(usage.line, /2 left/);
  });

  it("shows GST on a purchase and a plain message when the hour was taken", () => {
    assert.equal(
      gstLine({
        purchase: { subtotal_cad: "40.00", gst_rate: "0.05", gst_cad: "2.00", total_cad: "42.00" },
      }),
      "Subtotal $40.00 · GST $2.00 · total $42.00",
    );
    assert.equal(gstLine({ pricing_rule: { hours: "1" } }), null);
    assert.equal(
      bookingErrorCopy("hoist_overlap", "That bay already has a booking on this hour."),
      "That hour was just taken. Pick another time.",
    );
    assert.equal(bookingErrorCopy("other", "Try again."), "Try again.");
  });

  it("uses a day grid on a phone and a week grid on a desktop", () => {
    assert.equal(calendarViewForWidth(390), "day");
    assert.equal(calendarViewForWidth(767), "day");
    assert.equal(calendarViewForWidth(768), "week");
    assert.equal(calendarViewForWidth(1440), "week");
  });
});
