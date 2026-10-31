"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { ShopApiError } from "../../../lib/config";
import { buyMemberTokens } from "../../../lib/shop-api";

export async function buyTokensAction(formData: FormData): Promise<void> {
  try {
    await buyMemberTokens({
      payment_id: String(formData.get("payment_id") ?? "").trim(),
      tokens: String(formData.get("tokens") ?? "").trim(),
      subtotal_cad: String(formData.get("subtotal_cad") ?? "").trim(),
    });
  } catch (error) {
    const message = error instanceof ShopApiError ? error.message : "Could not buy tokens.";
    redirect(`/member/purchase?error=${encodeURIComponent(message)}`);
  }
  revalidatePath("/member");
  revalidatePath("/member/purchase");
  redirect("/member");
}
