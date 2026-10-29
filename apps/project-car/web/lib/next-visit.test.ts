import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

const libDir = dirname(fileURLToPath(import.meta.url));
const pagePath = join(libDir, "../app/member/page.tsx");
const cardPath = join(libDir, "../components/next-visit-card.tsx");

type Booking = {
  id: string;
  hoist_name: string;
  start_at: string;
  end_at: string;
  status: string;
};

function booking(overrides: Partial<Booking> & Pick<Booking, "id">): Booking {
  return {
    hoist_name: "Bay 2",
    start_at: "2026-06-17T20:00:00.000Z",
    end_at: "2026-06-17T22:00:00.000Z",
    status: "confirmed",
    ...overrides,
  };
}

describe("member home next visit", () => {
  it("test_member_home_renders_the_next_visit_card", () => {
    const page = readFileSync(pagePath, "utf8");
    assert.match(
      page,
      /<NextVisitCard\b/,
      "member home must render the Next visit card",
    );
    assert.match(
      page,
      /<NextVisitCard[\s\S]*bookings=\{me\.bookings\}[\s\S]*now=\{shopClock\(\)\}/,
      "the card must use the bookings and shop clock the page already has",
    );

    const card = readFileSync(cardPath, "utf8");
    assert.match(card, />Next visit</, "the card must be titled Next visit");
    assert.match(card, /nextVisit\(bookings,\s*now\)/, "the card must ask nextVisit for the row");
    assert.match(card, /\{visit\.bay\}/, "the card must show the bay");
    assert.match(card, /\{visit\.dayLabel\}/, "the card must show the shop day");
    assert.match(card, /\{visit\.timeLabel\}/, "the card must show the shop time");
    assert.match(card, /\{visit\.status\}/, "the card must show the status");
    assert.match(card, /\{visit\.checkInOpensLabel\}/, "the card must show when check-in opens");
    assert.match(card, /\{NO_VISIT_BOOKED\}/, "an empty card must say No visit booked");
    assert.match(card, /href=\{SCHEDULE_HREF\}/, "an empty card must link to the member schedule");
  });
});

describe("nextVisit", () => {
  it("test_next_visit_picks_the_earliest_future_booking_and_skips_past_and_cancelled", async () => {
    // Regina is UTC−6. This instant is 12:00 on Wednesday 2026-06-17.
    const now = new Date("2026-06-17T18:00:00.000Z");
    const past = booking({
      id: "past",
      hoist_name: "Bay 1",
      start_at: "2026-06-17T15:00:00.000Z",
      end_at: "2026-06-17T17:00:00.000Z",
      status: "completed",
    });
    const endsAtNow = booking({
      id: "ends-at-now",
      hoist_name: "Bay 6",
      start_at: "2026-06-17T16:00:00.000Z",
      end_at: now.toISOString(),
      status: "confirmed",
    });
    const cancelled = booking({
      id: "cancelled",
      hoist_name: "Bay 3",
      start_at: "2026-06-17T19:00:00.000Z",
      end_at: "2026-06-17T21:00:00.000Z",
      status: "cancelled",
    });
    const later = booking({
      id: "later",
      hoist_name: "Bay 4",
      start_at: "2026-06-18T02:00:00.000Z",
      end_at: "2026-06-18T04:00:00.000Z",
      status: "pending",
    });
    const earliest = booking({
      id: "earliest",
      hoist_name: "Bay 2",
      start_at: "2026-06-17T20:00:00.000Z",
      end_at: "2026-06-17T22:00:00.000Z",
      status: "confirmed",
    });
    const underway = booking({
      id: "underway",
      hoist_name: "Bay 5",
      start_at: "2026-06-17T17:00:00.000Z",
      end_at: "2026-06-17T19:30:00.000Z",
      status: "active",
    });
    const unreadable = booking({
      id: "unreadable",
      hoist_name: "Bay 9",
      start_at: "not-a-time",
      end_at: "also-not",
      status: "confirmed",
    });

    const helper = await loadNextVisit();
    const order = [later, past, cancelled, endsAtNow, unreadable, earliest];
    const ids = order.map((row) => row.id);
    const visit = helper.nextVisit(order, now);
    assert.deepEqual(
      order.map((row) => row.id),
      ids,
      "nextVisit must not reorder the bookings the home page also lists",
    );
    assert.ok(visit, "a future booking must be the next visit");
    assert.equal(visit.id, "earliest");
    assert.equal(visit.bay, "Bay 2");
    assert.equal(visit.status, "confirmed");

    const current = helper.nextVisit([earliest, underway], now);
    assert.equal(current?.id, "underway", "a visit that has started and not ended is not past");
    assert.equal(current?.status, "active");

    assert.equal(helper.nextVisit([past, endsAtNow, cancelled, unreadable], now), null);
    assert.equal(helper.nextVisit([], now), null);
  });

  it("test_next_visit_window_is_start_minus_15_minutes_in_america_regina", async () => {
    const now = new Date("2026-06-17T18:00:00.000Z");
    // 02:00Z is 20:00 the previous calendar day in America/Regina, not 18 June.
    const startAt = "2026-06-18T02:00:00.000Z";
    const endAt = "2026-06-18T04:00:00.000Z";
    const helper = await loadNextVisit();
    assert.equal(helper.NEXT_VISIT_EARLY_MINUTES, 15);
    assert.equal(helper.NO_VISIT_BOOKED, "No visit booked");
    assert.equal(helper.SCHEDULE_HREF, "/member/schedule");

    const visit = helper.nextVisit(
      [
        booking({
          id: "regina",
          hoist_name: "Bay 4",
          start_at: startAt,
          end_at: endAt,
          status: "pending",
        }),
      ],
      now,
    );
    assert.ok(visit);
    assert.equal(visit.bay, "Bay 4");
    assert.equal(visit.status, "pending");
    assert.equal(visit.dayLabel, "Wed, Jun 17");
    assert.equal(visit.timeLabel, "20:00–22:00");
    assert.equal(new Date(visit.opensAt).getTime(), new Date(startAt).getTime() - 15 * 60 * 1000);
    assert.equal(visit.opensAt, "2026-06-18T01:45:00.000Z");
    assert.equal(visit.checkInOpensLabel, "Check-in opens at 19:45");
  });
});

async function loadNextVisit(): Promise<{
  nextVisit: (
    bookings: readonly Booking[],
    now: Date,
  ) => {
    id: string;
    bay: string;
    status: string;
    dayLabel: string;
    timeLabel: string;
    opensAt: string;
    checkInOpensLabel: string;
  } | null;
  NEXT_VISIT_EARLY_MINUTES: number;
  NO_VISIT_BOOKED: string;
  SCHEDULE_HREF: string;
}> {
  try {
    return await import("./next-visit.ts");
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    assert.fail(`nextVisit is not on this tree: ${message}`);
  }
}
