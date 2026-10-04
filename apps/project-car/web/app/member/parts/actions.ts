"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { ShopApiError } from "../../../lib/config";
import { createMemberPartsRequest } from "../../../lib/shop-api";

function bounce(error: unknown): never {
  const message = error instanceof ShopApiError ? error.message : "Parts request failed.";
  redirect(`/member/parts?error=${encodeURIComponent(message)}`);
}

export async function createMemberPartsRequestAction(formData: FormData): Promise<void> {
  try {
    await createMemberPartsRequest({
      sku: String(formData.get("sku") ?? "").trim(),
      note: String(formData.get("note") ?? "").trim() || undefined,
    });
  } catch (error) {
    bounce(error);
  }
  revalidatePath("/member/parts");
  revalidatePath("/parts");
  redirect("/member/parts");
}
