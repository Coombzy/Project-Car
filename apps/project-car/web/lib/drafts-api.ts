import { shopJson } from "./shop-api";
import { pathSegment } from "./shop-path";
import type { StaffDraft } from "./drafts-view";

export function listStaffDrafts(): Promise<StaffDraft[]> {
  return shopJson<StaffDraft[]>("/staff/drafts", "Could not load drafts.");
}

export function acceptFillDraft(id: string): Promise<unknown> {
  return shopJson(`/fill/drafts/${pathSegment(id)}/accept`, "Could not accept the fill draft.", { method: "POST" });
}

export function acceptChatDraft(id: string): Promise<unknown> {
  return shopJson(`/chat/drafts/${pathSegment(id)}/accept`, "Could not accept the chat draft.", { method: "POST" });
}
