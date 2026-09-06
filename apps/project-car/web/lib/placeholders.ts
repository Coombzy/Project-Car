/** Demo-only copy for Parts / Job board / Cameras. Not live APIs. */

export const PRIMARY_CAMERA_ID = "cam-shop-main";

export const SAMPLE_PARTS = [
  {
    id: "part-caliper-bracket",
    name: "Wilwood caliper bracket (sample)",
    note: "Member/customer parts desk — not a catalog and not for sale.",
    status: "Coming later",
  },
  {
    id: "part-an-fittings",
    name: "AN fittings assortment (sample)",
    note: "Full purchase + eBay stay Later (pc.marketplace off).",
    status: "Coming later",
  },
  {
    id: "part-shop-towels",
    name: "Shop towels — case (sample)",
    note: "Placeholder so people can see what this surface is about.",
    status: "Coming later",
  },
] as const;

export const SAMPLE_JOBS = [
  {
    id: "job-sweep-floor",
    title: "Sweep the shop floor",
    area: "Shop floor",
    needed: "Tonight after last booking",
    note: "Broom and dustpan by the west door.",
  },
  {
    id: "job-empty-oil",
    title: "Empty the used-oil drum",
    area: "Waste",
    needed: "When the drum is at the line",
    note: "Staff confirm the recycler pickup — members do not haul off-site.",
  },
  {
    id: "job-restock-towels",
    title: "Restock shop towels",
    area: "Consumables",
    needed: "Bay cabinets 1–5",
    note: "Towels live on the north shelf. Do not open a sealed case without ops.",
  },
  {
    id: "job-sort-fasteners",
    title: "Sort leftover fasteners",
    area: "Tool wall",
    needed: "Whenever you have 20 minutes",
    note: "Keep metric and SAE split. Unknown hardware goes in the mystery bin.",
  },
  {
    id: "job-take-out-recycling",
    title: "Break down cardboard",
    area: "Receiving",
    needed: "After parts deliveries",
    note: "Flatten and stack by the rear door. Claim / complete is Later.",
  },
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
