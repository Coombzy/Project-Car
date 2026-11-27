"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { ShopApiError } from "../../lib/config";
import { acceptRefundRequest } from "../../lib/refunds-api";

export async function acceptRefundRequestAction(formData: FormData): Promise<void> {
  const id = String(formData.get("id") ?? "");
  try {
    await acceptRefundRequest(id);
  } catch (error) {
    const message = error instanceof ShopApiError ? error.message : "Could not accept the refund request.";
    redirect(`/refund-requests?error=${encodeURIComponent(message)}`);
  }
  revalidatePath("/refund-requests");
  redirect(`/refund-requests?notice=${encodeURIComponent("Refund request accepted.")}`);
}
