"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { parseJobForm } from "../../lib/job-form";
import { jobPostDecision } from "../../lib/job-post";
import { createShopJob } from "../../lib/jobs-api";

export async function postJobAction(formData: FormData): Promise<void> {
  const parsed = parseJobForm({
    title: formData.get("title"),
    notes: formData.get("notes"),
    bounty: formData.get("bounty"),
  });
  const planned = jobPostDecision({ type: "parsed", parsed });
  if (planned.kind === "redirect") {
    redirect(planned.href);
  }
  try {
    await createShopJob(planned.body);
  } catch (error) {
    redirect(jobPostDecision({ type: "rejected", error }).href);
  }
  const posted = jobPostDecision({ type: "created" });
  revalidatePath(posted.revalidate);
  redirect(posted.href);
}
