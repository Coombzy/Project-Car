import { MemberRequestDesk } from "../../../components/member-request-desk";
import { MemberShell } from "../../../components/member-shell";
import { PlaceholderNote } from "../../../components/placeholder-note";
import { handleMemberPageError } from "../../../lib/page";
import { getMemberMe } from "../../../lib/shop-api";

export const dynamic = "force-dynamic";

export default async function MemberPartsPage() {
  try {
    const me = await getMemberMe();
    return (
      <MemberShell email={me.email} current="parts">
        <MemberPartsBody />
      </MemberShell>
    );
  } catch (error) {
    const message = await handleMemberPageError(error);
    return (
      <MemberShell current="parts">
        <MemberPartsBody />
        <div className="banner error">{message}</div>
      </MemberShell>
    );
  }
}

function MemberPartsBody() {
  return (
    <>
      <p className="eyebrow">Customer-facing · placeholder</p>
      <h1>Parts &amp; tool requests</h1>
      <p className="lede">
        Ask ops for a shop-stock part (<code>PT-…</code>) or a specialty crib
        tool (<code>TC-…</code>). This is a request desk — not a catalog, not
        checkout, not eBay. Bay kits (B1–B6) stay on the hoist; members do not
        shop those. No Stripe. The shop is not open.
      </p>
      <PlaceholderNote>
        Customer-facing placeholder on temporary <code>app.</code>{" "}
        <code>/member</code> — migrates to projectcar.ca later. Sample SKUs
        only. Requests, not purchasing. Flag <code>pc.marketplace</code> stays
        off.
      </PlaceholderNote>
      <MemberRequestDesk />
    </>
  );
}
