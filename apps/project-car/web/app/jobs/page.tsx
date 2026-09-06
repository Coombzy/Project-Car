import { JobBoard } from "../../components/job-board";
import { OwnerShell } from "../../components/owner-shell";
import { PlaceholderNote } from "../../components/placeholder-note";
import { handlePageError } from "../../lib/page";
import { getMe } from "../../lib/shop-api";

export const dynamic = "force-dynamic";

export default async function OpsJobsPage() {
  try {
    const me = await getMe();
    return (
      <OwnerShell email={me.email} current="jobs" wide>
        <OpsJobsBody />
      </OwnerShell>
    );
  } catch (error) {
    const message = await handlePageError(error);
    return (
      <OwnerShell current="jobs" wide>
        <OpsJobsBody />
        <div className="banner error">{message}</div>
      </OwnerShell>
    );
  }
}

function OpsJobsBody() {
  return (
    <>
      <p className="eyebrow">Ops · placeholder</p>
      <h1>Job board</h1>
      <p className="lede">
        Ops posts shop upkeep (cleaning, tool maintenance, random tasks) with a{" "}
        <strong>token bounty</strong>. When a member completes a job, tokens
        credit their account on the append-only ledger — same token system as
        hoist booking, not Stripe. Claim / complete stay Later; the bounty
        column is the model lock.
      </p>
      <PlaceholderNote>
        Sample jobs with token amounts. Buttons do not post, claim, or move
        ledger tokens. Not a live work-order system. Host{" "}
        <code>ops.projectcar.ca</code> (temporary <code>app.</code> alias still
        up).
      </PlaceholderNote>
      <JobBoard audience="ops" />
    </>
  );
}
