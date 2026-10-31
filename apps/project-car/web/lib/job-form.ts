/** A posted bounty is above 0 and at most 10,000 tokens, with at most two decimal places.
 * `ShopJobCreate.token_bounty` on origin/main is still `ge=0` with no upper bound (`schemas.py`). */
export const JOB_BOUNTY_CAP = 10_000;

const TITLE_ERROR = "Enter a title.";
const BOUNTY_ERROR =
  "A job bounty is 0 to 10,000 tokens, with at most two decimal places.";

const CAP_CENTS = JOB_BOUNTY_CAP * 100;

export type ParsedJobForm =
  | { ok: true; title: string; notes: string | null; token_bounty: string }
  | { ok: false; error: string };

function text(value: unknown): string | null {
  return typeof value === "string" ? value : null;
}

function parseBounty(raw: string): string | null {
  const match = /^(\d+)(?:\.(\d+))?$/.exec(raw.trim());
  if (!match) {
    return null;
  }
  const whole = (match[1] ?? "").replace(/^0+(?=\d)/, "") || "0";
  const significant = (match[2] ?? "").replace(/0+$/, "");
  if (significant.length > 2) {
    return null;
  }
  const wholeNum = Number(whole);
  const fracCents = significant.length === 0 ? 0 : Number(significant.padEnd(2, "0"));
  if (!Number.isSafeInteger(wholeNum) || !Number.isSafeInteger(fracCents)) {
    return null;
  }
  const cents = wholeNum * 100 + fracCents;
  if (!Number.isSafeInteger(cents) || cents <= 0 || cents > CAP_CENTS) {
    return null;
  }
  return significant.length === 0 ? whole : `${whole}.${significant}`;
}

export function parseJobForm(input: {
  title: unknown;
  notes?: unknown;
  bounty: unknown;
}): ParsedJobForm {
  const titleRaw = text(input.title);
  if (titleRaw === null || titleRaw.trim().length === 0) {
    return { ok: false, error: TITLE_ERROR };
  }
  const bountyRaw = text(input.bounty);
  const tokenBounty = bountyRaw === null ? null : parseBounty(bountyRaw);
  if (tokenBounty === null) {
    return { ok: false, error: BOUNTY_ERROR };
  }
  const notesRaw = text(input.notes);
  const notes = notesRaw === null ? null : notesRaw.trim() || null;
  return { ok: true, title: titleRaw.trim(), notes, token_bounty: tokenBounty };
}

export const JOB_POSTED_NOTICE = "Job posted.";
export const JOB_POST_FAILURE = "Could not post the job.";

export function jobPostedHref(): string {
  return `/jobs?notice=${encodeURIComponent(JOB_POSTED_NOTICE)}`;
}

export function jobErrorHref(message: string): string {
  return `/jobs?error=${encodeURIComponent(message)}`;
}
