import assert from "node:assert/strict";
import { describe, it } from "node:test";

import {
  OPEN_SHOP_HOURS,
  addMonths,
  bookedHoursOnDay,
  bookingHourPlacement,
  calendarDate,
  densityLevel,
  hoistChipLabel,
  hoistDayDensity,
  isOccupyingStatus,
  monthGrid,
  monthOf,
  monthWindow,
  overlapHours,
  parseShopInstant,
  parseHoistParam,
  parseMonthParam,
  parseSlotParam,
  parseViewParam,
  scheduleHref,
  slotEnd,
  sortHoists,
  zonedDateTime,
} from "./calendar.ts";

describe("densityLevel", () => {
  it("returns empty for zero or invalid booked hours", () => {
    assert.equal(densityLevel(0), "empty");
    assert.equal(densityLevel(-1), "empty");
    assert.equal(densityLevel(Number.NaN), "empty");
    assert.equal(densityLevel(2, 0), "empty");
  });

  it("maps booked hours vs 13 open shop hours", () => {
    assert.equal(OPEN_SHOP_HOURS, 13);
    assert.equal(densityLevel(1), "light");
    assert.equal(densityLevel(3.24), "light");
    assert.equal(densityLevel(3.25), "medium");
    assert.equal(densityLevel(6.49), "medium");
    assert.equal(densityLevel(6.5), "heavy");
    assert.equal(densityLevel(9.74), "heavy");
    assert.equal(densityLevel(9.75), "full");
    assert.equal(densityLevel(13), "full");
    assert.equal(densityLevel(20), "full");
  });
});

describe("occupying status", () => {
  it("treats cancelled as free and other live statuses as occupying", () => {
    assert.equal(isOccupyingStatus("cancelled"), false);
    assert.equal(isOccupyingStatus("pending"), true);
    assert.equal(isOccupyingStatus("confirmed"), true);
    assert.equal(isOccupyingStatus("active"), true);
    assert.equal(isOccupyingStatus("completed"), true);
    assert.equal(isOccupyingStatus("overdue"), true);
  });
});

describe("America/Regina bounds", () => {
  it("maps Regina midnight to UTC−6", () => {
    assert.equal(zonedDateTime("2026-09-08", 0).toISOString(), "2026-09-08T06:00:00.000Z");
    assert.equal(zonedDateTime("2026-09-08", 9).toISOString(), "2026-09-08T15:00:00.000Z");
    assert.equal(zonedDateTime("2026-01-15", 8).toISOString(), "2026-01-15T14:00:00.000Z");
  });

  it("labels a UTC instant on the Regina calendar date", () => {
    assert.equal(calendarDate("2026-09-08T06:00:00.000Z"), "2026-09-08");
    assert.equal(calendarDate("2026-09-08T05:59:00.000Z"), "2026-09-07");
  });

  it("treats naive API timestamps as Regina wall clock, not UTC", () => {
    assert.equal(parseShopInstant("2026-09-08T09:00:00").toISOString(), "2026-09-08T15:00:00.000Z");
    assert.equal(calendarDate("2026-09-08T09:00:00"), "2026-09-08");
    const placement = bookingHourPlacement("2026-09-08T09:00:00", "2026-09-08T12:00:00", "2026-09-08");
    assert.ok(placement);
    assert.equal(placement.startHour, 9);
    assert.equal(placement.endHour, 12);
  });
});

describe("booked hours and density", () => {
  const hoist = "11111111-1111-4111-8111-111111111111";

  it("clips a booking to the Regina calendar day", () => {
    const hours = bookedHoursOnDay(
      [
        {
          hoist_id: hoist,
          start_at: "2026-09-08T15:00:00.000Z",
          end_at: "2026-09-08T18:00:00.000Z",
          status: "confirmed",
        },
      ],
      hoist,
      "2026-09-08",
    );
    assert.equal(hours, 3);
  });

  it("ignores cancelled bookings and other hoists", () => {
    const hours = bookedHoursOnDay(
      [
        {
          hoist_id: hoist,
          start_at: "2026-09-08T15:00:00.000Z",
          end_at: "2026-09-08T20:00:00.000Z",
          status: "cancelled",
        },
        {
          hoist_id: "22222222-2222-4222-8222-222222222222",
          start_at: "2026-09-08T15:00:00.000Z",
          end_at: "2026-09-08T18:00:00.000Z",
          status: "confirmed",
        },
      ],
      hoist,
      "2026-09-08",
    );
    assert.equal(hours, 0);
  });

  it("splits a booking that crosses midnight", () => {
    const interval = {
      hoist_id: hoist,
      start_at: "2026-09-09T04:00:00.000Z",
      end_at: "2026-09-09T08:00:00.000Z",
      status: "confirmed",
    };
    assert.equal(bookedHoursOnDay([interval], hoist, "2026-09-08"), 2);
    assert.equal(bookedHoursOnDay([interval], hoist, "2026-09-09"), 2);
  });

  it("returns light density for a typical 3-hour seed slot", () => {
    const density = hoistDayDensity(
      [
        {
          hoist_id: hoist,
          start_at: "2026-09-08T15:00:00.000Z",
          end_at: "2026-09-08T18:00:00.000Z",
          status: "confirmed",
        },
      ],
      hoist,
      "2026-09-08",
    );
    assert.equal(density.bookedHours, 3);
    assert.equal(density.level, "light");
    assert.ok(Math.abs(density.ratio - 3 / 13) < 1e-9);
  });
});

describe("overlapHours", () => {
  it("returns zero when windows do not overlap", () => {
    const start = zonedDateTime("2026-09-08", 8);
    const end = zonedDateTime("2026-09-08", 21);
    assert.equal(overlapHours("2026-09-07T00:00:00.000Z", "2026-09-07T01:00:00.000Z", start, end), 0);
  });
});

describe("bookingHourPlacement", () => {
  it("places a 09:00–12:00 Regina booking in the day column", () => {
    const placement = bookingHourPlacement(
      "2026-09-08T15:00:00.000Z",
      "2026-09-08T18:00:00.000Z",
      "2026-09-08",
    );
    assert.ok(placement);
    assert.equal(placement.startHour, 9);
    assert.equal(placement.endHour, 12);
    assert.equal(placement.topPct, (9 / 24) * 100);
    assert.equal(placement.heightPct, (3 / 24) * 100);
  });

  it("returns null when the booking is on another day", () => {
    assert.equal(
      bookingHourPlacement("2026-09-08T15:00:00.000Z", "2026-09-08T18:00:00.000Z", "2026-09-09"),
      null,
    );
  });
});

describe("month grid", () => {
  it("starts September 2026 on Monday 31 August", () => {
    const weeks = monthGrid("2026-09");
    assert.equal(weeks[0][0], "2026-08-31");
    assert.equal(weeks[0][1], "2026-09-01");
    assert.equal(weeks[weeks.length - 1][6] >= "2026-09-30", true);
    assert.equal(monthOf("2026-09-08"), "2026-09");
    assert.equal(addMonths("2026-09", 1), "2026-10");
    assert.equal(addMonths("2026-01", -1), "2025-12");
    const window = monthWindow("2026-09");
    assert.equal(window.start, "2026-08-31");
    assert.equal(window.end > "2026-09-30", true);
  });
});

describe("param and label helpers", () => {
  it("parses view, month, hoist, and slot safely", () => {
    assert.equal(parseViewParam(undefined), "month");
    assert.equal(parseViewParam("week"), "week");
    assert.equal(parseViewParam("nope"), "month");
    assert.equal(parseViewParam(undefined, "2026-09-07"), "week");
    assert.equal(parseViewParam("month", "2026-09-07"), "month");
    assert.equal(parseMonthParam("2026-09"), "2026-09");
    assert.equal(parseMonthParam("2026-13", "2026-09-08"), "2026-09");
    assert.equal(parseHoistParam("11111111-1111-4111-8111-111111111111"), "11111111-1111-4111-8111-111111111111");
    assert.equal(parseHoistParam("not-a-uuid"), undefined);
    assert.equal(parseSlotParam("2026-09-08T09:00"), "2026-09-08T09:00");
    assert.equal(parseSlotParam("2026-09-08 09:00"), undefined);
    assert.equal(slotEnd("2026-09-08T09:00"), "2026-09-08T10:00");
  });

  it("builds schedule hrefs and hoist labels", () => {
    assert.equal(
      scheduleHref("/schedule", { view: "week", week: "2026-09-07", hoist: "abc" }),
      "/schedule?view=week&week=2026-09-07&hoist=abc",
    );
    assert.equal(hoistChipLabel("Bay 3", false), "B3");
    assert.equal(hoistChipLabel("Shop", true), "Shop");
    const sorted = sortHoists([
      { name: "Shop", is_shop: true },
      { name: "Bay 2", is_shop: false },
      { name: "Bay 1", is_shop: false },
    ]);
    assert.deepEqual(
      sorted.map((row) => row.name),
      ["Bay 1", "Bay 2", "Shop"],
    );
  });
});
