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
        Members pick up tasks that need doing around the shop. Ops sees the same
        sample board. Claim, assign, and complete stay Later — buttons do
        nothing.
      </p>
      <PlaceholderNote>
        Sample tasks only. Not a live work-order system. Intended host{" "}
        <code>ops.projectcar.ca</code> (today the temporary <code>app.</code>{" "}
        alias).
      </PlaceholderNote>
      <JobBoard audience="ops" />
    </>
  );
}
