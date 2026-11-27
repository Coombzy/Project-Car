"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { createMemberPartsRequest } from "../../../lib/shop-api";

const MISSING_SKU_MESSAGE = "Enter a part number.";
const FAILURE_MESSAGE = "Parts request failed.";

// The error argument is kept for the call site. Its text can carry internal
// detail, so only a fixed message ever reaches the query string.
function bounce(error: unknown): never {
  redirect(`/member/parts?error=${encodeURIComponent(FAILURE_MESSAGE)}`);
}

export async function createMemberPartsRequestAction(formData: FormData): Promise<void> {
  const sku = String(formData.get("sku") ?? "").trim();
  if (!sku) {
    redirect(`/member/parts?error=${encodeURIComponent(MISSING_SKU_MESSAGE)}`);
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
