import { MemberShell } from "../../../components/member-shell";
import { handleMemberPageError } from "../../../lib/page";
import { getMemberMe } from "../../../lib/shop-api";
import { PurchaseForm } from "./purchase-form";

export const dynamic = "force-dynamic";

export default async function MemberPurchasePage({
  searchParams,
}: {
  searchParams: Promise<{ error?: string }>;
}) {
  const params = await searchParams;
  try {
    const me = await getMemberMe();
    return (
      <MemberShell email={me.email} current="purchase">
        <p className="eyebrow">Buy tokens</p>
        <h1>Buy tokens</h1>
        <p className="lede">
          GST is 5% of the before-tax amount. The stand-in payment adapter records a STANDIN id.
          A real processor can replace that adapter later. The shop is not open.
        </p>
        {params.error ? <div className="banner error">{params.error}</div> : null}
        <section className="card">
          <PurchaseForm />
        </section>
      </MemberShell>
    );
  } catch (error) {
    const message = await handleMemberPageError(error);
    return (
      <MemberShell current="purchase">
        <h1>Buy tokens</h1>
        <div className="banner error">{message}</div>
      </MemberShell>
    );
  }
}
