"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { ShopApiError } from "../../lib/config";
import { checkoutCribTool, returnCribTool } from "../../lib/shop-api";

function bounce(error: unknown, fallback: string): never {
  const message = error instanceof ShopApiError ? error.message : fallback;
  redirect(`/tools?kit=TC&error=${encodeURIComponent(message)}`);
}

export async function checkoutCribToolAction(formData: FormData): Promise<void> {
  try {
    await checkoutCribTool({
      member_id: String(formData.get("member_id") ?? "").trim(),
      sku: String(formData.get("sku") ?? "").trim(),
      note: String(formData.get("note") ?? "").trim() || undefined,
    });
  } catch (error) {
    bounce(error, "Tool checkout failed.");
  }
  revalidatePath("/tools");
  redirect("/tools?kit=TC");
}

export async function returnCribToolAction(formData: FormData): Promise<void> {
  try {
    await returnCribTool({
      sku: String(formData.get("sku") ?? "").trim(),
      note: String(formData.get("note") ?? "").trim() || undefined,
    });
  } catch (error) {
    bounce(error, "Tool return failed.");
  }
  revalidatePath("/tools");
  redirect("/tools?kit=TC");
}
