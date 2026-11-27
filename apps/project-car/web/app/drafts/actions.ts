"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { ShopApiError } from "../../lib/config";
import { acceptChatDraft, acceptFillDraft } from "../../lib/drafts-api";

export async function acceptDraftAction(formData: FormData): Promise<void> {
  const id = String(formData.get("id") ?? "");
  const kind = String(formData.get("kind") ?? "");
  try {
    if (kind === "chat") await acceptChatDraft(id);
    else if (kind === "fill") await acceptFillDraft(id);
    else throw new Error("Could not accept the draft.");
  } catch (error) {
    const message = error instanceof ShopApiError ? error.message : "Could not accept the draft.";
    redirect(`/drafts?error=${encodeURIComponent(message)}`);
  }
  revalidatePath("/drafts");
  redirect(`/drafts?notice=${encodeURIComponent("Draft accepted.")}`);
}
