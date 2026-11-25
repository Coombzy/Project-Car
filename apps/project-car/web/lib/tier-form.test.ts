import assert from "node:assert/strict";
import { describe, it } from "node:test";

import { parseTierForm } from "./tier-form.ts";

const good = {
  name: "premium-plus",
  display_name: "Premium Plus",
  price: "99.99",
  included_tokens: "400",
  booking_window_days: "14",
  max_simultaneous_bookings: "2",
};

describe("parseTierForm", () => {
  it("refuses a blank name and a 3-decimal price", () => {
    for (const name of ["", "  ", "\n\t"]) {
      assert.equal(parseTierForm({ ...good, name }).ok, false);
    }
    assert.equal(parseTierForm({ ...good, price: "10.125" }).ok, false);
  });

  it("refuses a blank display name, pricing, 10000, and bad integers", () => {
    const refused = [
      { display_name: "" },
      { display_name: "   " },
      { name: "pricing" },
      { name: " Pricing " },
      { name: "PRICING" },
      { price: "10000" },
      { included_tokens: "" },
      { included_tokens: null },
      { included_tokens: "100001" },
      { included_tokens: "-1" },
      { booking_window_days: "0" },
      { booking_window_days: "366" },
      { booking_window_days: "14.5" },
      { max_simultaneous_bookings: "" },
      { max_simultaneous_bookings: "21" },
    ];
    for (const patch of refused) {
      assert.equal(parseTierForm({ ...good, ...patch }).ok, false);
    }
  });

  it("parses a good form to the POST /tiers field set", () => {
    assert.deepEqual(
      parseTierForm({
        name: "Premium-Plus",
        display_name: " Premium Plus ",
        price: "99.99",
        included_tokens: "400",
        booking_window_days: "14",
        max_simultaneous_bookings: "2",
        notes: "  bay 2  ",
      }),
      {
        ok: true,
        name: "premium-plus",
        display_name: "Premium Plus",
        price: "99.99",
        included_tokens: 400,
        booking_window_days: 14,
        max_simultaneous_bookings: 2,
        notes: "bay 2",
      },
    );
    const bare = parseTierForm(good);
    assert.equal(bare.ok, true);
    if (bare.ok) {
      assert.equal(bare.notes, null);
    }
    assert.equal(
      parseTierForm({
        ...good,
        price: "9999.99",
        included_tokens: "0",
        booking_window_days: "365",
        max_simultaneous_bookings: "20",
        notes: "   ",
      }).ok,
      true,
    );
  });
});
