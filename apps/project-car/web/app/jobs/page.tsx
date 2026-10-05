import { JobBoard } from "../../components/job-board";
import { JobLedger } from "../../components/job-ledger";
import { OwnerShell } from "../../components/owner-shell";
import { PlaceholderNote } from "../../components/placeholder-note";
import type { JobEvent } from "../../lib/config";
import { handlePageError } from "../../lib/page";
import { getMe, listJobEvents } from "../../lib/shop-api";

export const dynamic = "force-dynamic";

export default async function OpsJobsPage() {
  try {
    const me = await getMe();
    const events = await listJobEvents();
    return (
      <OwnerShell email={me.email} current="jobs" wide>
        <OpsJobsBody events={events} />
      </OwnerShell>
    );
  } catch (error) {
    const message = await handlePageError(error);
    return (
      <OwnerShell current="jobs" wide>
        <OpsJobsBody events={[]} />
        <div className="banner error">{message}</div>
      </OwnerShell>
    );
  }
}

function OpsJobsBody({ events }: { events: JobEvent[] }) {
  return (
    <>
      <p className="eyebrow">Ops</p>
      <h1>Job board</h1>
      <p className="lede">
        Members claim a posted job and mark it done. Each of those stores a row.
        Done does not credit the token ledger. Posting a new job stays later.
        The shop is not open.
      </p>
      <PlaceholderNote>
        Sample jobs stay labeled as a sample below this note. The ledger is the
        stored claim and done rows. Sample buttons do not post, assign, or move
        tokens. The shop is not open.
      </PlaceholderNote>
      <JobLedger audience="ops" events={events} />
      <h2>Sample board (not stored)</h2>
      <JobBoard audience="ops" />
    </>
  );
}
