"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { ShopApiError } from "../../lib/config";
import { decideRequest } from "../../lib/requests-api";
import type { RequestKind } from "../../lib/requests-view";
const KINDS: Record<string, RequestKind> = { shop_hoist: "shop_hoist", parts: "parts", tool_crib: "tool_crib" };

export async function decideRequestAction(formData: FormData): Promise<void> {
  const id = String(formData.get("id") ?? "");
  const kind = KINDS[String(formData.get("kind") ?? "")];
  const raw = String(formData.get("decision") ?? "");
  const decision = raw === "approve" || raw === "deny" ? raw : null;
  if (!kind || !decision || id === "") redirect(`/requests?error=${encodeURIComponent("Could not update the request.")}`);
  try {
    await decideRequest(kind, id, decision);
  } catch (error) {
    const message = error instanceof ShopApiError ? error.message : "Could not update the request.";
    redirect(`/requests?error=${encodeURIComponent(message)}`);
  }
  revalidatePath("/requests");
  redirect(`/requests?notice=${encodeURIComponent(decision === "approve" ? "Approved." : "Denied.")}`);
}
