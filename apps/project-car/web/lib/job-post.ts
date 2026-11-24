/** Owner job-post redirect. No sibling imports: node --test and tsc disagree on the suffix. */

const JOB_POSTED_NOTICE = "Job posted.";
const JOB_POST_FAILURE = "Could not post the job.";

type ParsedJob =
  | { ok: true; title: string; notes: string | null; token_bounty: string }
  | { ok: false; error: string };

type JobBody = { title: string; notes: string | null; token_bounty: string };

function shopApiMessage(error: unknown): string | null {
  if (!(error instanceof Error) || error.name !== "ShopApiError") {
    return null;
  }
  const branded = error as { status?: unknown; code?: unknown };
  if (typeof branded.status !== "number" || typeof branded.code !== "string") {
    return null;
  }
  return error.message;
}

type ParsedEvent = { type: "parsed"; parsed: ParsedJob };
type RejectedEvent = { type: "rejected"; error: unknown };
type CreatedEvent = { type: "created" };
type JobEvent = ParsedEvent | RejectedEvent | CreatedEvent;

export function jobPostDecision(
  event: ParsedEvent,
): { kind: "redirect"; href: string } | { kind: "create"; body: JobBody };
export function jobPostDecision(event: RejectedEvent): { kind: "redirect"; href: string };
export function jobPostDecision(
  event: CreatedEvent,
): { kind: "posted"; revalidate: "/jobs"; href: string };
export function jobPostDecision(
  event: JobEvent,
):
  | { kind: "redirect"; href: string }
  | { kind: "create"; body: JobBody }
  | { kind: "posted"; revalidate: "/jobs"; href: string } {
  switch (event.type) {
    case "parsed":
      if (!event.parsed.ok) {
        return { kind: "redirect", href: `/jobs?error=${encodeURIComponent(event.parsed.error)}` };
      }
      return {
        kind: "create",
        body: {
          title: event.parsed.title,
          notes: event.parsed.notes,
          token_bounty: event.parsed.token_bounty,
        },
      };
    case "rejected":
      return {
        kind: "redirect",
        href: `/jobs?error=${encodeURIComponent(shopApiMessage(event.error) ?? JOB_POST_FAILURE)}`,
      };
    case "created":
      return {
        kind: "posted",
        revalidate: "/jobs",
        href: `/jobs?notice=${encodeURIComponent(JOB_POSTED_NOTICE)}`,
      };
    default: {
      const unexpected: never = event;
      return unexpected;
    }
  }
}
