export type RefundRequestRow = {
  id: string;
  booking_id: string;
  status: string;
  created_by_kind: string;
  created_by_id: string;
};

export function refundRows(input: unknown): RefundRequestRow[] {
  if (!Array.isArray(input)) return [];
  const rows: RefundRequestRow[] = [];
  for (const item of input) {
    if (typeof item !== "object" || item === null || Array.isArray(item)) continue;
    const id = (item as { id?: unknown }).id;
    if (typeof id !== "string" || id === "") continue;
    rows.push(item as RefundRequestRow);
  }
  return rows;
}
