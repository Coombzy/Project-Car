import { MemberRequestDesk } from "../../../components/member-request-desk";
import { MemberShell } from "../../../components/member-shell";
import { PlaceholderNote } from "../../../components/placeholder-note";
import type { PartsRequest } from "../../../lib/config";
import { handleMemberPageError } from "../../../lib/page";
import { getMemberMe, listMemberPartsRequests } from "../../../lib/shop-api";
import { createMemberPartsRequestAction } from "./actions";

export const dynamic = "force-dynamic";

export default async function MemberPartsPage({
  searchParams,
}: {
  searchParams?: Promise<{ error?: string }>;
}) {
  const query = searchParams ? await searchParams : {};
  try {
    const me = await getMemberMe();
    const requests = await listMemberPartsRequests();
    return (
      <MemberShell email={me.email} current="parts">
        <MemberPartsBody requests={requests} error={query.error} />
      </MemberShell>
    );
  } catch (error) {
    const message = await handleMemberPageError(error);
    return (
      <MemberShell current="parts">
        <MemberPartsBody requests={[]} error={query.error} />
        <div className="banner error">{message}</div>
      </MemberShell>
    );
  }
}

function MemberPartsBody({
  requests,
  error,
}: {
  requests: PartsRequest[];
  error?: string;
}) {
  return (
    <>
      <p className="eyebrow">Customer-facing</p>
      <h1>Parts requests</h1>
      <p className="lede">
        Ask ops for a shop-stock part (<code>PT-…</code>). Sending the form
        stores a row. This is a request desk — not a catalog, not checkout,
        not eBay. Crib tools (<code>TC-…</code>) and bay kits (B1–B6) do not
        check out here. No Stripe. The shop is not open.
      </p>
      {error ? <div className="banner error">{error}</div> : null}
      <PlaceholderNote>
        Customer-facing request desk on temporary <code>app.</code>{" "}
        <code>/member</code> — migrates to projectcar.ca later. A stored parts
        request is one row, not purchasing. Flag <code>pc.marketplace</code>{" "}
        stays off.
      </PlaceholderNote>
      <MemberRequestDesk requests={requests} create={createMemberPartsRequestAction} />
    </>
  );
}
