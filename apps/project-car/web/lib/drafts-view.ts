export type StaffDraft = { id: string; kind: "fill" | "chat"; status: string; body: string; room_id: string | null };

export type DraftRow = { draft: StaffDraft; roomHref: string | null };

export function draftRows(drafts: StaffDraft[]): DraftRow[] {
  const rows: DraftRow[] = [];
  for (const draft of drafts) {
    if (draft.kind === "fill") rows.push({ draft, roomHref: null });
    else if (draft.kind === "chat") rows.push({ draft, roomHref: draft.room_id ? `/chat/${encodeURIComponent(draft.room_id)}` : null });
  }
  return rows;
}
