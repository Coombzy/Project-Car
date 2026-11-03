import { JobBoard } from "../../components/job-board";
import { JobLedger } from "../../components/job-ledger";
import { OwnerShell } from "../../components/owner-shell";
import { PlaceholderNote } from "../../components/placeholder-note";
import { PostJobForm } from "../../components/post-job-form";
import type { JobEvent } from "../../lib/config";
import { handlePageError } from "../../lib/page";
import { getMe, listJobEvents } from "../../lib/shop-api";

export const dynamic = "force-dynamic";

export default async function OpsJobsPage({
  searchParams,
}: {
  searchParams: Promise<{ error?: string; notice?: string }>;
}) {
  try {
    const params = await searchParams;
    const me = await getMe();
    const events = await listJobEvents();
    return (
      <OwnerShell email={me.email} current="jobs" wide>
        <OpsJobsBody events={events} error={params.error} notice={params.notice} />
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

function OpsJobsBody({
  events,
  error,
  notice,
}: {
  events: JobEvent[];
  error?: string;
  notice?: string;
}) {
  return (
    <>
      <p className="eyebrow">Ops</p>
      <h1>Job board</h1>
      <p className="lede">
        Members claim a posted job and mark it done. Each of those stores a row.
        Done does not credit the token ledger. Post a job from this page. The shop
        is not open.
      </p>
      {error ? <div className="banner error">{error}</div> : null}
      {notice ? <div className="banner empty">{notice}</div> : null}
      <PostJobForm />
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
