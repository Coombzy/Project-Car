import assert from "node:assert/strict";
import { describe, it } from "node:test";

import {
  checkInOpensAt,
  nextVisit,
  NEXT_VISIT_EARLY_MINUTES,
  NO_VISIT_BOOKED,
  SCHEDULE_HREF,
} from "./next-visit.ts";

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

describe("nextVisit", () => {
  it("test_next_visit_picks_the_earliest_future_booking_and_skips_past_and_cancelled", () => {
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

    const order = [later, past, cancelled, endsAtNow, unreadable, earliest];
    const ids = order.map((row) => row.id);
    const visit = nextVisit(order, now);
    assert.deepEqual(
      order.map((row) => row.id),
      ids,
      "nextVisit must not reorder the bookings the home page also lists",
    );
    assert.ok(visit, "a future booking must be the next visit");
    assert.equal(visit.id, "earliest");
    assert.equal(visit.bay, "Bay 2");
    assert.equal(visit.status, "confirmed");

    const current = nextVisit([earliest, underway], now);
    assert.equal(current?.id, "underway", "a visit that has started and not ended is not past");
    assert.equal(current?.status, "active");

    assert.equal(nextVisit([past, endsAtNow, cancelled, unreadable], now), null);
    assert.equal(nextVisit([], now), null);
  });

  it("test_next_visit_window_is_start_minus_15_minutes_in_america_regina", () => {
    const now = new Date("2026-06-17T18:00:00.000Z");
    // 02:00Z is 20:00 the previous calendar day in America/Regina, not 18 June.
    const startAt = "2026-06-18T02:00:00.000Z";
    const endAt = "2026-06-18T04:00:00.000Z";
    assert.equal(NEXT_VISIT_EARLY_MINUTES, 15);
    assert.equal(NO_VISIT_BOOKED, "No visit booked");
    assert.equal(SCHEDULE_HREF, "/member/schedule");

    const visit = nextVisit(
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

  it("test_next_visit_check_in_opens_15_minutes_before_an_in_progress_visit", () => {
    // Backlog proof: 10:00–11:00 with now 10:10, and nothing later, is the next visit.
    // America/Regina is UTC−6. 10:00 Regina is 16:00Z; 10:10 is 16:10Z.
    const now = new Date("2026-06-17T16:10:00.000Z");
    assert.equal(typeof checkInOpensAt, "function");
    assert.equal(NEXT_VISIT_EARLY_MINUTES, 15);

    const inProgress = booking({
      id: "in-progress",
      hoist_name: "Bay 1",
      start_at: "2026-06-17T16:00:00.000Z",
      end_at: "2026-06-17T17:00:00.000Z",
      status: "confirmed",
    });
    const later = booking({
      id: "later-same-day",
      hoist_name: "Bay 2",
      start_at: "2026-06-17T18:00:00.000Z",
      end_at: "2026-06-17T20:00:00.000Z",
      status: "confirmed",
    });
    const opens = checkInOpensAt(inProgress.start_at);
    assert.equal(opens.toISOString(), "2026-06-17T15:45:00.000Z");

    const visit = nextVisit([later, inProgress], now);
    assert.ok(visit, "a visit that has started and not ended is the next visit");
    assert.equal(visit.id, "in-progress");
    assert.equal(visit.bay, "Bay 1");
    assert.equal(visit.status, "confirmed");
    assert.equal(visit.dayLabel, "Wed, Jun 17");
    assert.equal(visit.timeLabel, "10:00–11:00");
    assert.equal(visit.checkInOpensLabel, "Check-in opens at 09:45");
    assert.equal(visit.opensAt, opens.toISOString());
  });

  it("test_next_visit_breaks_ties_by_end_then_id", () => {
    const now = new Date("2026-06-17T18:00:00.000Z");
    const laterEnd = booking({
      id: "a-later-end",
      start_at: "2026-06-17T20:00:00.000Z",
      end_at: "2026-06-17T23:00:00.000Z",
    });
    const earlierEnd = booking({
      id: "b-earlier-end",
      start_at: "2026-06-17T20:00:00.000Z",
      end_at: "2026-06-17T21:00:00.000Z",
    });
    const byEnd = nextVisit([laterEnd, earlierEnd], now);
    assert.equal(byEnd?.id, "b-earlier-end");

    const zee = booking({ id: "zee", start_at: "2026-06-17T20:00:00.000Z", end_at: "2026-06-17T22:00:00.000Z" });
    const aye = booking({ id: "aye", start_at: "2026-06-17T20:00:00.000Z", end_at: "2026-06-17T22:00:00.000Z" });
    const byId = nextVisit([zee, aye], now);
    assert.equal(byId?.id, "aye");
  });
});
