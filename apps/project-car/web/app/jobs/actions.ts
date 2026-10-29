"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { ShopApiError } from "../../lib/config";
import { parseJobForm } from "../../lib/job-form";
import { createShopJob } from "../../lib/jobs-api";

function bounce(error: unknown): never {
  const message = error instanceof ShopApiError ? error.message : "Could not post the job.";
  redirect(`/jobs?error=${encodeURIComponent(message)}`);
}

export async function postJobAction(formData: FormData): Promise<void> {
  const parsed = parseJobForm({
    title: formData.get("title"),
    notes: formData.get("notes"),
    bounty: formData.get("bounty"),
  });
  if (!parsed.ok) {
    redirect(`/jobs?error=${encodeURIComponent(parsed.error)}`);
  }
  try {
    await createShopJob({
      title: parsed.title,
      notes: parsed.notes,
      token_bounty: parsed.token_bounty,
    });
  } catch (error) {
    bounce(error);
  }
  revalidatePath("/jobs");
  redirect(`/jobs?notice=${encodeURIComponent("Job posted.")}`);
}
