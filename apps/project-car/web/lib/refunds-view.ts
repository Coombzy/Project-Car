export type RefundRequestRow = { id: string; booking_id: string; status: string; created_by_kind: string; created_by_id: string };

function text(value: unknown): string | null {
  return typeof value === "string" ? value : null;
}

export function refundRows(input: unknown): RefundRequestRow[] {
  if (!Array.isArray(input)) return [];
  const rows: RefundRequestRow[] = [];
  for (const item of input) {
    if (typeof item !== "object" || item === null || Array.isArray(item)) continue;
    const raw = item as Record<string, unknown>;
    const id = text(raw.id), booking_id = text(raw.booking_id), status = text(raw.status), created_by_kind = text(raw.created_by_kind), created_by_id = text(raw.created_by_id);
    if (!id || booking_id === null || status === null || created_by_kind === null || created_by_id === null) continue;
    rows.push({ id, booking_id, status, created_by_kind, created_by_id });
  }
  return rows;
}
