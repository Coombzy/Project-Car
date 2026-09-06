/** Demo-only copy for Job board / Cameras / Payments. Inventory SKUs live in inventory.ts. */

export const PRIMARY_CAMERA_ID = "cam-shop-main";

export const SAMPLE_JOBS = [
  {
    id: "job-sweep-floor",
    title: "Sweep the shop floor",
    kind: "Cleaning",
    area: "Shop floor",
    needed: "Tonight after last booking",
    tokenBounty: 25,
    note: "Ops-posted bounty. Credit hits the member ledger on complete — not Stripe.",
  },
  {
    id: "job-empty-oil",
    title: "Empty the used-oil drum",
    kind: "Upkeep",
    area: "Waste",
    needed: "When the drum is at the line",
    tokenBounty: 40,
    note: "Staff confirm the recycler pickup — members do not haul off-site.",
  },
  {
    id: "job-restock-towels",
    title: "Restock shop towels",
    kind: "Upkeep",
    area: "Consumables",
    needed: "Bay cabinets 1–5",
    tokenBounty: 15,
    note: "Towels live on the north shelf. Do not open a sealed case without ops.",
  },
  {
    id: "job-torque-wrenches",
    title: "Check and oil torque wrenches",
    kind: "Tool maintenance",
    area: "Tool wall",
    needed: "This week",
    tokenBounty: 50,
    note: "Tag any wrench that is out of calibration. Claim / complete is Later.",
  },
  {
    id: "job-sort-fasteners",
    title: "Sort leftover fasteners",
    kind: "Upkeep",
    area: "Tool wall",
    needed: "Whenever you have 20 minutes",
    tokenBounty: 20,
    note: "Keep metric and SAE split. Unknown hardware goes in the mystery bin.",
  },
  {
    id: "job-take-out-recycling",
    title: "Break down cardboard",
    kind: "Cleaning",
    area: "Receiving",
    needed: "After parts deliveries",
    tokenBounty: 15,
    note: "Flatten and stack by the rear door.",
  },
] as const;

export const SAMPLE_MEMBERSHIP_PAYMENTS = [
  { id: "pay-m-1", who: "Ada Reyes", kind: "Membership — Premium", amount: "$ — sample", status: "Tracked by AI (ok)" },
  { id: "pay-m-2", who: "Sam Okonkwo", kind: "Membership — Basic", amount: "$ — sample", status: "Tracked by AI (ok)" },
  { id: "pay-m-3", who: "Jordan Hale", kind: "Membership — Basic", amount: "$ — sample", status: "Exception — alert ops" },
] as const;

export const SAMPLE_PARTS_PAYMENTS = [
  { id: "pay-p-1", who: "Ada Reyes", kind: "Parts — caliper bracket", amount: "$ — sample", status: "Tracked by AI (ok)" },
  { id: "pay-p-2", who: "Shop stock", kind: "Parts — AN fittings restock", amount: "$ — sample", status: "Tracked by AI (ok)" },
] as const;

export const SAMPLE_CAMERAS = [
  {
    id: PRIMARY_CAMERA_ID,
    name: "Shop floor — main",
    location: "Center aisle, looking west",
    primary: true,
    hint: "Primary member camera. Occupancy from this feed is a hint, not bay truth.",
  },
  {
    id: "cam-bay-1",
    name: "Bay 1",
    location: "North wall",
    primary: false,
    hint: "Ops-only in v1. Booking calendar is still the source of truth.",
  },
  {
    id: "cam-bay-2",
    name: "Bay 2",
    location: "North wall",
    primary: false,
    hint: "Ops-only in v1.",
  },
  {
    id: "cam-parking",
    name: "Parking lot",
    location: "Exterior, lot",
    primary: false,
    hint: "Ops-only. Vehicle events are AI stubs, not live NVR.",
  },
  {
    id: "cam-front-door",
    name: "Front door",
    location: "Entry vestibule",
    primary: false,
    hint: "Ops-only. Door logs are a separate stub below.",
  },
  {
    id: "cam-rear",
    name: "Rear shop",
    location: "Receiving / waste",
    primary: false,
    hint: "Ops-only.",
  },
] as const;

export const SAMPLE_DOOR_LOGS = [
  {
    id: "door-1",
    at: "2026-09-06 07:12",
    who: "Ada Reyes (sample)",
    door: "Front door",
    result: "Unlock granted (stub)",
  },
  {
    id: "door-2",
    at: "2026-09-06 07:14",
    who: "Staff on shift (sample)",
    door: "Rear shop",
    result: "Unlock granted (stub)",
  },
  {
    id: "door-3",
    at: "2026-09-06 08:02",
    who: "Unknown fob (sample)",
    door: "Front door",
    result: "Denied (stub)",
  },
] as const;

export const SAMPLE_AI_EVENTS = [
  {
    id: "ai-1",
    at: "2026-09-06 08:40",
    camera: "Shop floor — main",
    kind: "Person",
    note: "Frigate-style stub. Occupancy hint — not hoist source of truth.",
  },
  {
    id: "ai-2",
    at: "2026-09-06 09:05",
    camera: "Parking lot",
    kind: "Vehicle",
    note: "AI collection stub. No live NVR in this PR.",
  },
  {
    id: "ai-3",
    at: "2026-09-06 10:18",
    camera: "Bay 1",
    kind: "Occupancy hint",
    note: "Hint only. Calendar / booking rows still own the bay.",
  },
] as const;

export function primaryCamera() {
  return SAMPLE_CAMERAS.find((camera) => camera.primary) ?? SAMPLE_CAMERAS[0];
}
