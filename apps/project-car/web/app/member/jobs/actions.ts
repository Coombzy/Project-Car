"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { ShopApiError } from "../../../lib/config";
import { claimJob, markJobDone } from "../../../lib/shop-api";

function bounce(error: unknown, fallback: string): never {
  const message = error instanceof ShopApiError ? error.message : fallback;
  redirect(`/member/jobs?error=${encodeURIComponent(message)}`);
}

export async function claimJobAction(formData: FormData): Promise<void> {
  try {
    await claimJob({
      job_key: String(formData.get("job_key") ?? "").trim(),
      note: String(formData.get("note") ?? "").trim() || undefined,
    });
  } catch (error) {
    bounce(error, "Job claim failed.");
  }
  revalidatePath("/member/jobs");
  revalidatePath("/jobs");
  redirect("/member/jobs");
}

export async function markJobDoneAction(formData: FormData): Promise<void> {
  try {
    await markJobDone({
      job_key: String(formData.get("job_key") ?? "").trim(),
      note: String(formData.get("note") ?? "").trim() || undefined,
    });
  } catch (error) {
    bounce(error, "Job done failed.");
  }
  revalidatePath("/member/jobs");
  revalidatePath("/jobs");
  redirect("/member/jobs");
}
