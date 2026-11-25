export type RequestKind = "shop_hoist" | "parts" | "tool_crib";
type Row = Record<string, unknown>;
export type OpenStaffRequests = { shop_hoist: Row[]; parts: Row[]; tool_crib: Row[] } & Record<string, unknown>;
export type RequestGroup = { kind: RequestKind; label: "Shop hoist" | "Parts" | "Tool crib"; rows: Row[] };
const ORDER: { kind: RequestKind; label: RequestGroup["label"] }[] = [
  { kind: "shop_hoist", label: "Shop hoist" },
  { kind: "parts", label: "Parts" },
  { kind: "tool_crib", label: "Tool crib" },
];

export function groupRequests(input: OpenStaffRequests & Record<string, unknown>): RequestGroup[] {
  const groups: RequestGroup[] = [];
  for (const spec of ORDER) {
    const raw = input[spec.kind];
    if (!Array.isArray(raw) || raw.length === 0) continue;
    const rows = raw as Row[];
    const list = spec.kind === "shop_hoist" ? [...rows].sort((a, b) => String(a.created_at ?? "").localeCompare(String(b.created_at ?? ""))) : rows;
    groups.push({ kind: spec.kind, label: spec.label, rows: list });
  }
  return groups;
}
