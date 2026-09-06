import { MemberShell } from "../../../components/member-shell";
import { PartsCatalog } from "../../../components/parts-catalog";
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
      <h1>Parts purchasing</h1>
      <p className="lede">
        Buy parts through the shop when this desk is live. This page is a
        temporary stand-in so you can see what it is about. Full checkout and
        eBay stay Later. No Stripe. The shop is not open.
      </p>
      <PlaceholderNote>
        Customer-facing placeholder on temporary <code>app.</code>{" "}
        <code>/member</code> — migrates to projectcar.ca later. Sample cards
        only. Not live purchasing.
      </PlaceholderNote>
      <PartsCatalog audience="member" />
    </>
  );
}
