import { JobBoard } from "../../../components/job-board";
import { JobLedger } from "../../../components/job-ledger";
import { MemberShell } from "../../../components/member-shell";
import { PlaceholderNote } from "../../../components/placeholder-note";
import type { JobEvent } from "../../../lib/config";
import { handleMemberPageError } from "../../../lib/page";
import { getMemberMe, listMemberJobEvents } from "../../../lib/shop-api";

export const dynamic = "force-dynamic";

export default async function MemberJobsPage({
  searchParams,
}: {
  searchParams: Promise<{ error?: string }>;
}) {
  const params = await searchParams;
  try {
    const me = await getMemberMe();
    const events = await listMemberJobEvents();
    return (
      <MemberShell email={me.email} current="jobs" wide>
        <MemberJobsBody events={events} error={params.error} />
      </MemberShell>
    );
  } catch (error) {
    const message = await handleMemberPageError(error);
    return (
      <MemberShell current="jobs" wide>
        <MemberJobsBody events={[]} error={params.error} />
        <div className="banner error">{message}</div>
      </MemberShell>
    );
  }
}

function MemberJobsBody({ events, error }: { events: JobEvent[]; error?: string }) {
  return (
    <>
      <p className="eyebrow">Customer-facing</p>
      <h1>Job board</h1>
      <p className="lede">
        Shop upkeep — cleaning, tool maintenance, random tasks. A claim stores
        one row. Marking that job done stores a second row. Done does not credit
        your token ledger. The shop is not open.
      </p>
      <PlaceholderNote>
        Customer-facing job board on <code>/member/jobs</code>. The sample table
        is not the stored rows. Claim and done do not move tokens.
      </PlaceholderNote>
      <JobLedger audience="member" events={events} error={error} />
      <h2>Sample board (not stored)</h2>
      <JobBoard audience="member" />
    </>
  );
}
