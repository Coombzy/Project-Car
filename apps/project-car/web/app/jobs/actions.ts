"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { ShopApiError } from "../../lib/config";
import { JOB_POST_FAILURE, jobErrorHref, jobPostedHref, parseJobForm } from "../../lib/job-form";
import { createShopJob } from "../../lib/jobs-api";

function bounce(error: unknown): never {
  const message = error instanceof ShopApiError ? error.message : JOB_POST_FAILURE;
  redirect(jobErrorHref(message));
}

export async function postJobAction(formData: FormData): Promise<void> {
  const parsed = parseJobForm({
    title: formData.get("title"),
    notes: formData.get("notes"),
    bounty: formData.get("bounty"),
  });
  if (!parsed.ok) {
    redirect(jobErrorHref(parsed.error));
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
  redirect(jobPostedHref());
}
