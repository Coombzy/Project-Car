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
        Tasks that need doing around the shop — sweep, restock, sort. Claim and
        complete stay Later. These are sample jobs so the board is visible.
      </p>
      <PlaceholderNote>
        Customer-facing placeholder on temporary <code>app.</code>{" "}
        <code>/member</code>. Buttons do not claim work.
      </PlaceholderNote>
      <JobBoard audience="member" />
    </>
  );
}
