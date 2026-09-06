import { OwnerShell } from "../../components/owner-shell";
import { PartsCatalog } from "../../components/parts-catalog";
import { PlaceholderNote } from "../../components/placeholder-note";
import { handlePageError } from "../../lib/page";
import { getMe } from "../../lib/shop-api";

export const dynamic = "force-dynamic";

export default async function OpsPartsPage() {
  try {
    const me = await getMe();
    return (
      <OwnerShell email={me.email} current="parts">
        <OpsPartsBody />
      </OwnerShell>
    );
  } catch (error) {
    const message = await handlePageError(error);
    return (
      <OwnerShell current="parts">
        <OpsPartsBody />
        <div className="banner error">{message}</div>
      </OwnerShell>
    );
  }
}

function OpsPartsBody() {
  return (
    <>
      <p className="eyebrow">Ops · placeholder</p>
      <h1>Parts purchasing</h1>
      <p className="lede">
        Members / customers will buy parts through the shop. This ops page is a
        temporary stand-in so staff can see the surface. Full purchase and eBay
        stay Later. Flag <code>pc.marketplace</code> stays off. No Stripe. The
        shop is not open.
      </p>
      <PlaceholderNote>
        Placeholder catalog — sample cards only. Not live purchasing, not eBay,
        not a price list.
      </PlaceholderNote>
      <PartsCatalog audience="ops" />
    </>
  );
}
