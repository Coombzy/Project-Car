import Link from "next/link";

import { OwnerShell } from "../../components/owner-shell";
import { listStaffDrafts } from "../../lib/drafts-api";
import { draftRows } from "../../lib/drafts-view";
import { handlePageError } from "../../lib/page";
import { getMe } from "../../lib/shop-api";
import { acceptDraftAction } from "./actions";

export const dynamic = "force-dynamic";

export default async function DraftsPage({ searchParams }: { searchParams: Promise<{ error?: string; notice?: string }> }) {
  try {
    const params = await searchParams;
    const me = await getMe();
    const rows = draftRows(await listStaffDrafts());
    return (
      <OwnerShell email={me.email} current="drafts">
        <p className="eyebrow">GET /staff/drafts</p>
        <h1>Drafts</h1>
        <p className="lede">Pending fill notices and chat replies. Accept posts the draft. The shop is not open.</p>
        {params.error ? <div className="banner error">{params.error}</div> : null}
        {params.notice ? <div className="banner empty">{params.notice}</div> : null}
        {rows.length === 0 ? <p>No pending drafts.</p> : rows.map((row) => (
          <section className="card" key={row.draft.id} style={{ marginTop: "1rem" }}>
            <p className="eyebrow">{row.draft.kind === "chat" ? "Chat" : "Fill"}</p>
            <div className="chat-bubble"><p>{row.draft.body}</p></div>
            {row.roomHref ? <p><Link href={row.roomHref}>Open room</Link></p> : null}
            <form action={acceptDraftAction}>
              <input type="hidden" name="id" value={row.draft.id} /><input type="hidden" name="kind" value={row.draft.kind} />
              <button type="submit">Accept</button>
            </form>
          </section>
        ))}
      </OwnerShell>
    );
  } catch (error) {
    const message = await handlePageError(error);
    return <OwnerShell current="drafts"><h1>Drafts</h1><div className="banner error">{message}</div></OwnerShell>;
  }
}
