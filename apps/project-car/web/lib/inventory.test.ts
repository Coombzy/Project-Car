import assert from "node:assert/strict";
import { describe, it } from "node:test";

import {
  BAY_PREFIXES,
  SAMPLE_BAY_KIT_ITEMS,
  SAMPLE_CRIB_TOOLS,
  SAMPLE_INVENTORY_REQUESTS,
  SAMPLE_OPS_PART_ORDERS,
  SAMPLE_PARTS_STOCK,
  SAMPLE_TOOL_ORDERS,
  SHOP_HOIST_BAY,
  checkoutLabel,
  formatSku,
  isBayPrefix,
  parseKitParam,
  parseSku,
  partsReorderState,
} from "./inventory.ts";

describe("SKU shape PREFIX-CATEGORY-NNN", () => {
  it("accepts locked examples", () => {
    assert.deepEqual(parseSku("B2-WR-014"), {
      sku: "B2-WR-014",
      prefix: "B2",
      category: "WR",
      serial: "014",
    });
    assert.deepEqual(parseSku("TC-TQ-003"), {
      sku: "TC-TQ-003",
      prefix: "TC",
      category: "TQ",
      serial: "003",
    });
    assert.deepEqual(parseSku("PT-OIL-5W30-012"), {
      sku: "PT-OIL-5W30-012",
      prefix: "PT",
      category: "OIL-5W30",
      serial: "012",
    });
    assert.equal(parseSku("cm-tw-001")?.prefix, "CM");
  });

  it("rejects shop-hoist SH prefix and broken shapes", () => {
    assert.equal(parseSku("SH-WR-001"), null);
    assert.equal(parseSku("B7-WR-001"), null);
    assert.equal(parseSku("B2-wr-14"), null);
    assert.equal(parseSku("B2-WR-14"), null);
    assert.equal(parseSku("TOOL-001"), null);
  });

  it("formats padded serials", () => {
    assert.equal(formatSku("B6", "WR", 1), "B6-WR-001");
    assert.equal(formatSku("PT", "OIL-5W30", "12"), "PT-OIL-5W30-012");
  });
});

describe("prefix lock", () => {
  it("maps B6 to the shop hoist bay — not SH", () => {
    assert.equal(SHOP_HOIST_BAY, "B6");
    assert.deepEqual([...BAY_PREFIXES], ["B1", "B2", "B3", "B4", "B5", "B6"]);
    assert.equal(isBayPrefix("B6"), true);
    assert.equal(isBayPrefix("SH"), false);
    assert.equal(isBayPrefix("TC"), false);
  });

  it("parses kit query defaults and crib", () => {
    assert.equal(parseKitParam(undefined), "B1");
    assert.equal(parseKitParam("tc"), "TC");
    assert.equal(parseKitParam("B6"), "B6");
    assert.equal(parseKitParam("SH"), "B1");
  });
});

describe("placeholder demo SKUs", () => {
  it("gives every bay kit and crib/parts row a valid locked SKU", () => {
    const skus = [
      ...SAMPLE_BAY_KIT_ITEMS.map((row) => row.sku),
      ...SAMPLE_CRIB_TOOLS.map((row) => row.sku),
      ...SAMPLE_PARTS_STOCK.map((row) => row.sku),
      ...SAMPLE_INVENTORY_REQUESTS.map((row) => row.sku),
      ...SAMPLE_OPS_PART_ORDERS.map((row) => row.sku),
      ...SAMPLE_TOOL_ORDERS.map((row) => row.sku).filter(
        (sku): sku is string => sku !== null,
      ),
    ];
    for (const sku of skus) {
      const parsed = parseSku(sku);
      assert.ok(parsed, `invalid demo SKU ${sku}`);
    }
    assert.ok(SAMPLE_BAY_KIT_ITEMS.some((row) => row.bay === "B6"));
    assert.ok(SAMPLE_BAY_KIT_ITEMS.every((row) => !row.sku.startsWith("SH-")));
    assert.ok(SAMPLE_CRIB_TOOLS.every((row) => row.sku.startsWith("TC-")));
    assert.ok(SAMPLE_PARTS_STOCK.every((row) => row.sku.startsWith("PT-")));
  });

  it("marks crib checkout and parts reorder stubs", () => {
    assert.equal(checkoutLabel("overdue"), "Overdue (stub)");
    const oil = SAMPLE_PARTS_STOCK.find((row) => row.sku === "PT-OIL-5W30-012");
    assert.ok(oil);
    assert.equal(partsReorderState(oil), "reorder");
    const plenty = SAMPLE_PARTS_STOCK.find((row) => row.sku === "PT-FLT-001");
    assert.ok(plenty);
    assert.equal(partsReorderState(plenty), "ok");
  });
});
