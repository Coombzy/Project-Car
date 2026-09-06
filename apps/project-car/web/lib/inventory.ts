/** Locked inventory prefixes + placeholder demo SKUs. Not a live API. */

export const BAY_PREFIXES = ["B1", "B2", "B3", "B4", "B5", "B6"] as const;
export type BayPrefix = (typeof BAY_PREFIXES)[number];

export const CRIB_PREFIX = "TC";
export const PARTS_PREFIX = "PT";
export const CONSUMABLES_PREFIX = "CM";

export type ToolPrefix = BayPrefix | typeof CRIB_PREFIX;
export type InventoryPrefix =
  | ToolPrefix
  | typeof PARTS_PREFIX
  | typeof CONSUMABLES_PREFIX;

/** Shop hoist bay uses the same B-scheme as customer bays. Never SH. */
export const SHOP_HOIST_BAY: BayPrefix = "B6";

export const INVENTORY_PREFIXES = [
  ...BAY_PREFIXES,
  CRIB_PREFIX,
  PARTS_PREFIX,
  CONSUMABLES_PREFIX,
] as const;

/**
 * SKU shape: PREFIX-CATEGORY-NNN
 * CATEGORY may include extra hyphen segments (PT-OIL-5W30-012).
 */
export const SKU_PATTERN =
  /^(B[1-6]|TC|PT|CM)-([A-Z0-9]+(?:-[A-Z0-9]+)*)-(\d{3})$/;

export type ParsedSku = {
  sku: string;
  prefix: InventoryPrefix;
  category: string;
  serial: string;
};

export type CribCheckoutState = "available" | "checked_out" | "overdue";
export type BayKitState = "resident" | "missing";
export type ReorderState = "ok" | "reorder";

export type BayKitItem = {
  sku: string;
  name: string;
  category: string;
  bay: BayPrefix;
  state: BayKitState;
  note: string;
};

export type CribTool = {
  sku: string;
  name: string;
  category: string;
  checkout: CribCheckoutState;
  who: string | null;
  due: string | null;
  note: string;
};

export type PartsStock = {
  sku: string;
  name: string;
  category: string;
  qty: number;
  reorderPoint: number;
  unit: string;
  note: string;
};

export type InventoryRequest = {
  id: string;
  who: string;
  sku: string;
  what: string;
  kind: "part" | "crib_tool";
  status: string;
};

export type ToolOrder = {
  id: string;
  sku: string | null;
  what: string;
  vendor: string;
  status: string;
};

export type PlannedTool = {
  id: string;
  skuHint: string;
  what: string;
  note: string;
  when: string;
};

export const BAY_KITS: Record<
  BayPrefix,
  { prefix: BayPrefix; hoist: string; location: string; shopHoist: boolean }
> = {
  B1: { prefix: "B1", hoist: "Bay 1", location: "North wall", shopHoist: false },
  B2: { prefix: "B2", hoist: "Bay 2", location: "South wall", shopHoist: false },
  B3: { prefix: "B3", hoist: "Bay 3", location: "East wall", shopHoist: false },
  B4: { prefix: "B4", hoist: "Bay 4", location: "West wall", shopHoist: false },
  B5: { prefix: "B5", hoist: "Bay 5", location: "Center aisle", shopHoist: false },
  B6: {
    prefix: "B6",
    hoist: "Shop",
    location: "Internal / business work",
    shopHoist: true,
  },
};

const BAY_KIT_TEMPLATE = [
  { serial: "001", category: "WR", name: "Combination wrench set — SAE" },
  { serial: "002", category: "WR", name: "Combination wrench set — metric" },
  { serial: "001", category: "SK", name: "3/8 drive socket set" },
  { serial: "001", category: "PL", name: "Pliers assortment" },
  { serial: "001", category: "SC", name: "Screwdriver set" },
  { serial: "001", category: "HM", name: "Dead-blow hammer" },
] as const;

function bayNote(bay: BayPrefix, category: string): string {
  if (bay === "B6") {
    return "Shop-hoist resident kit (B6, not SH). Owner-only bay. Stays on the cart.";
  }
  if (bay === "B2" && category === "PL") {
    return "Placeholder missing row — kit is still bay-resident, not a crib checkout.";
  }
  return "Bay-resident hand tool. Does not check out through the crib.";
}

function bayState(bay: BayPrefix, category: string): BayKitState {
  return bay === "B2" && category === "PL" ? "missing" : "resident";
}

export const SAMPLE_BAY_KIT_ITEMS: BayKitItem[] = BAY_PREFIXES.flatMap((bay) =>
  BAY_KIT_TEMPLATE.map((item) => ({
    sku: formatSku(bay, item.category, item.serial),
    name: item.name,
    category: item.category,
    bay,
    state: bayState(bay, item.category),
    note: bayNote(bay, item.category),
  })),
);

export const SAMPLE_CRIB_TOOLS: CribTool[] = [
  {
    sku: "TC-TQ-003",
    name: "1/2 drive torque wrench",
    category: "TQ",
    checkout: "checked_out",
    who: "Ada Reyes (sample)",
    due: "2026-09-07 18:00",
    note: "Crib checkout stub — return / overdue later.",
  },
  {
    sku: "TC-TQ-004",
    name: "3/8 drive torque wrench",
    category: "TQ",
    checkout: "available",
    who: null,
    due: null,
    note: "Specialty crib tool. Not a bay-resident kit item.",
  },
  {
    sku: "TC-PR-001",
    name: "OTC ball-joint press",
    category: "PR",
    checkout: "overdue",
    who: "Sam Okonkwo (sample)",
    due: "2026-09-05 17:00",
    note: "Overdue stub. No QR / hardware in this slice.",
  },
  {
    sku: "TC-FL-001",
    name: "Flare-nut wrench set",
    category: "FL",
    checkout: "available",
    who: null,
    due: null,
    note: "Crib specialty. Members request; they do not buy it.",
  },
  {
    sku: "TC-EG-001",
    name: "Engine hoist",
    category: "EG",
    checkout: "checked_out",
    who: "Jordan Hale (sample)",
    due: "2026-09-08 12:00",
    note: "Checked-out stub. Still a crib tool, not B-prefix.",
  },
  {
    sku: "TC-MJ-002",
    name: "Slide hammer kit",
    category: "MJ",
    checkout: "available",
    who: null,
    due: null,
    note: "Placeholder crib row.",
  },
];

export const SAMPLE_PARTS_STOCK: PartsStock[] = [
  {
    sku: "PT-OIL-5W30-012",
    name: "Engine oil 5W-30 (jug)",
    category: "OIL-5W30",
    qty: 8,
    reorderPoint: 12,
    unit: "jug",
    note: "Below reorder — PO stub, not a live vendor ping.",
  },
  {
    sku: "PT-OIL-5W20-004",
    name: "Engine oil 5W-20 (jug)",
    category: "OIL-5W20",
    qty: 18,
    reorderPoint: 8,
    unit: "jug",
    note: "Shop stock. Members request; they do not check out.",
  },
  {
    sku: "PT-FLT-001",
    name: "Oil filter assortment",
    category: "FLT",
    qty: 24,
    reorderPoint: 10,
    unit: "ea",
    note: "Placeholder qty. Not a catalog price.",
  },
  {
    sku: "PT-ANF-008",
    name: "AN fittings assortment",
    category: "ANF",
    qty: 4,
    reorderPoint: 6,
    unit: "bin",
    note: "Below reorder. Distinct from member request desk.",
  },
  {
    sku: "PT-BRK-002",
    name: "Brake cleaner",
    category: "BRK",
    qty: 14,
    reorderPoint: 6,
    unit: "can",
    note: "Parts stock. Consumables (CM) stay Later.",
  },
  {
    sku: "PT-PAD-003",
    name: "Wilwood caliper bracket (sample)",
    category: "PAD",
    qty: 1,
    reorderPoint: 0,
    unit: "ea",
    note: "Member-requested line — not for sale on this page.",
  },
];

export const SAMPLE_INVENTORY_REQUESTS: InventoryRequest[] = [
  {
    id: "req-1",
    who: "Ada Reyes (sample)",
    sku: "PT-OIL-5W30-012",
    what: "Two jugs of 5W-30 for Saturday",
    kind: "part",
    status: "New (stub)",
  },
  {
    id: "req-2",
    who: "Sam Okonkwo (sample)",
    sku: "TC-EG-001",
    what: "Borrow engine hoist Saturday",
    kind: "crib_tool",
    status: "Review (stub)",
  },
  {
    id: "req-3",
    who: "Jordan Hale (sample)",
    sku: "PT-PAD-003",
    what: "Wilwood bracket when the next PO lands",
    kind: "part",
    status: "Linked to PO-1043 (stub)",
  },
];

export const SAMPLE_TOOL_ORDERS: ToolOrder[] = [
  {
    id: "to-1",
    sku: "TC-SK-010",
    what: "Replacement 1/2 impact sockets (crib)",
    vendor: "Harbor (sample)",
    status: "Open (stub)",
  },
  {
    id: "to-2",
    sku: "B3-SK-001",
    what: "Bay 3 socket set replacement (resident kit)",
    vendor: "McMaster (sample)",
    status: "Shipped (stub)",
  },
];

export const SAMPLE_TOOL_PLANNED: PlannedTool[] = [
  {
    id: "tp-1",
    skuHint: "B*-AR-001",
    what: "Second 2-post arm pad set (per-bay later)",
    note: "Would land as B-prefix resident items — not a PO yet",
    when: "Next quarter (stub)",
  },
  {
    id: "tp-2",
    skuHint: "TC-BC-001",
    what: "Blast cabinet",
    note: "Crib specialty if purchased. Member request cluster.",
    when: "Unscheduled (stub)",
  },
];

export const SAMPLE_OPS_PART_ORDERS = [
  {
    id: "po-1042",
    sku: "PT-ANF-008",
    what: "Shop-stock AN fittings restock",
    vendor: "Summit (sample)",
    for: "Shop inventory",
    status: "Ordered (stub)",
  },
  {
    id: "po-1043",
    sku: "PT-PAD-003",
    what: "Wilwood bracket — Ada Reyes",
    vendor: "Local parts (sample)",
    for: "Member request",
    status: "Incoming (stub)",
  },
  {
    id: "po-1044",
    sku: "PT-FLT-001",
    what: "Oil filter assortment — case",
    vendor: "Uline (sample)",
    for: "Shop inventory",
    status: "Received (stub)",
  },
] as const;

export function formatSku(
  prefix: InventoryPrefix,
  category: string,
  serial: string | number,
): string {
  const nnn = String(serial).padStart(3, "0");
  return `${prefix}-${category}-${nnn}`;
}

export function parseSku(value: string): ParsedSku | null {
  const match = SKU_PATTERN.exec(value.trim().toUpperCase());
  if (!match) {
    return null;
  }
  return {
    sku: match[0],
    prefix: match[1] as InventoryPrefix,
    category: match[2],
    serial: match[3],
  };
}

export function isBayPrefix(value: string): value is BayPrefix {
  return (BAY_PREFIXES as readonly string[]).includes(value);
}

export function isInventoryPrefix(value: string): value is InventoryPrefix {
  return (INVENTORY_PREFIXES as readonly string[]).includes(value);
}

export function parseKitParam(value?: string | null): ToolPrefix {
  const raw = (value ?? "B1").trim().toUpperCase();
  if (raw === CRIB_PREFIX) {
    return CRIB_PREFIX;
  }
  if (isBayPrefix(raw)) {
    return raw;
  }
  return "B1";
}

export function bayKitItems(bay: BayPrefix): BayKitItem[] {
  return SAMPLE_BAY_KIT_ITEMS.filter((item) => item.bay === bay);
}

export function partsReorderState(row: PartsStock): ReorderState {
  return row.qty <= row.reorderPoint ? "reorder" : "ok";
}

export function checkoutLabel(state: CribCheckoutState): string {
  if (state === "checked_out") {
    return "Checked out (stub)";
  }
  if (state === "overdue") {
    return "Overdue (stub)";
  }
  return "Available (stub)";
}

export function kitHref(kit: ToolPrefix): string {
  return `/tools?kit=${kit}`;
}
