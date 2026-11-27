"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { createMemberPartsRequest } from "../../../lib/shop-api";

const MISSING_SKU = "missing_sku";
const PARTS_REQUEST_FAILED = "parts_request_failed";

// The error argument is kept for the call site. Its text can carry internal
// detail, so only a fixed code ever reaches the query string.
function bounce(error: unknown): never {
  redirect(`/member/parts?error=${PARTS_REQUEST_FAILED}`);
}

export async function createMemberPartsRequestAction(formData: FormData): Promise<void> {
  const sku = String(formData.get("sku") ?? "").trim();
  if (!sku) {
    redirect(`/member/parts?error=${MISSING_SKU}`);
  }
  try {
    await createMemberPartsRequest({
      sku,
      note: String(formData.get("note") ?? "").trim() || undefined,
    });
  } catch (error) {
    bounce(error);
  }
  revalidatePath("/member/parts");
  revalidatePath("/parts");
  redirect("/member/parts");
}
