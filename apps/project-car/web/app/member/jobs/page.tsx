import { JobBoard } from "../../../components/job-board";
import { MemberShell } from "../../../components/member-shell";
import { PlaceholderNote } from "../../../components/placeholder-note";
import { handleMemberPageError } from "../../../lib/page";
import { getMemberMe } from "../../../lib/shop-api";

export const dynamic = "force-dynamic";

export default async function MemberJobsPage() {
  try {
    const me = await getMemberMe();
    return (
      <MemberShell email={me.email} current="jobs" wide>
        <MemberJobsBody />
      </MemberShell>
    );
  } catch (error) {
    const message = await handleMemberPageError(error);
    return (
      <MemberShell current="jobs" wide>
        <MemberJobsBody />
        <div className="banner error">{message}</div>
      </MemberShell>
    );
  }
}

function MemberJobsBody() {
  return (
    <>
      <p className="eyebrow">Customer-facing · placeholder</p>
      <h1>Job board</h1>
      <p className="lede">
        Shop upkeep — cleaning, tool maintenance, random tasks. Ops posts each
        job with a <strong>token bounty</strong>. Completing one credits your
        token ledger (append-only, not Stripe). Claim / complete stay Later;
        amounts are visible so the model is clear.
      </p>
      <PlaceholderNote>
        Customer-facing placeholder on <code>/member/jobs</code>. Sample
        bounties only. Buttons do not claim, complete, or move tokens.
      </PlaceholderNote>
      <JobBoard audience="member" />
    </>
  );
}
