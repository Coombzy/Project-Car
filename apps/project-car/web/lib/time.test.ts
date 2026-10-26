import assert from "node:assert/strict";
import { describe, it } from "node:test";

import { addDays, mondayOf, parseWeekParam, shopDateTimeLocal, tokensLabel } from "./time.ts";

// America/Regina is UTC−6 all year. This instant is 12:30 on Wednesday 2026-06-17,
// so the current shop week starts Monday 2026-06-15. shopClock reads
// NEXT_PUBLIC_SHOP_NOW first; clear it so the freeze is SHOP_NOW.
delete process.env.NEXT_PUBLIC_SHOP_NOW;
process.env.SHOP_NOW = "2026-06-17T18:30:00.000Z";

const CURRENT_SHOP_WEEK = "2026-06-15";

describe("addDays", () => {
  it("test_add_days_crosses_month_and_year_ends", () => {
    assert.equal(addDays("2026-01-31", 1), "2026-02-01");
    assert.equal(addDays("2026-03-01", -1), "2026-02-28");
    assert.equal(addDays("2026-12-31", 1), "2027-01-01");
    assert.equal(addDays("2027-01-01", -1), "2026-12-31");
  });
});

describe("mondayOf", () => {
  it("test_monday_of_a_sunday_and_a_monday", () => {
    assert.equal(mondayOf("2026-06-21"), "2026-06-15");
    assert.equal(mondayOf("2026-06-15"), "2026-06-15");
  });
});

describe("parseWeekParam", () => {
  it("test_parse_week_param_real_dates_answer_their_monday", () => {
    assert.equal(parseWeekParam("2026-06-15"), "2026-06-15");
    assert.equal(parseWeekParam("2026-06-17"), "2026-06-15");
    assert.equal(parseWeekParam("2026-06-21"), "2026-06-15");
    assert.equal(parseWeekParam("2026-02-28"), "2026-02-23");
    assert.equal(parseWeekParam("2024-02-29"), "2024-02-26");
  });

  it("test_parse_week_param_missing_value_is_the_current_shop_week", () => {
    assert.equal(parseWeekParam(undefined), CURRENT_SHOP_WEEK);
    assert.equal(parseWeekParam(""), CURRENT_SHOP_WEEK);
    assert.equal(parseWeekParam("not-a-date"), CURRENT_SHOP_WEEK);
  });

  it("test_parse_week_param_impossible_dates_fall_back_to_the_current_shop_week", () => {
    // Each of these matches /^\d{4}-\d{2}-\d{2}$/ and Date.UTC rolls it into another week.
    const weeks = ["2026-02-31", "2026-13-01", "2026-04-31", "2026-02-29", "2026-00-15", "2026-06-00"];
    const actual = Object.fromEntries(weeks.map((week) => [week, parseWeekParam(week)]));
    const expected = Object.fromEntries(weeks.map((week) => [week, CURRENT_SHOP_WEEK]));
    assert.deepEqual(actual, expected);
  });
});

describe("tokensLabel", () => {
  it("test_tokens_label_integers_fractions_and_non_numeric", () => {
    assert.equal(tokensLabel(100), "100");
    assert.equal(tokensLabel("90"), "90");
    assert.equal(tokensLabel(180.5), "180.50");
    assert.equal(tokensLabel("180.50"), "180.50");
    assert.equal(tokensLabel(-1.5), "-1.50");
    assert.equal(tokensLabel("nope"), "nope");
  });
});

describe("shopDateTimeLocal", () => {
  it("test_shop_date_time_local_uses_the_frozen_shop_clock", () => {
    assert.equal(shopDateTimeLocal(), "2026-06-17T12:30");
    assert.equal(shopDateTimeLocal(new Date("2026-06-17T06:00:00.000Z")), "2026-06-17T00:00");
  });
});
