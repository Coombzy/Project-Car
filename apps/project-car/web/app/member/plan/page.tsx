import { PlanOffer } from "../../../components/plan-offer";
import { MemberShell } from "../../../components/member-shell";
import { handleMemberPageError } from "../../../lib/page";
import { getMemberMe, listPublicPlans } from "../../../lib/shop-api";

export const dynamic = "force-dynamic";

export default async function MemberPlanPage() {
  try {
    let me;
    try {
      me = await getMemberMe();
    } catch (error) {
      const message = await handleMemberPageError(error);
      return (
        <MemberShell current="plan">
          <h1>Your plan</h1>
          <div className="banner error">{message}</div>
        </MemberShell>
      );
    }
    const plans = await listPublicPlans();
    const yours = plans.find((plan) => plan.name === me.tier_name);
    return (
      <MemberShell email={me.email} current="plan">
        <p className="eyebrow">Plans</p>
        <h1>Your plan</h1>
        <p className="lede">
          Prices are the saved monthly amounts plus GST. The owner edits them.
          The shop is not open.
        </p>
        {yours ? (
          <p className="muted">
            You are on {yours.display_name}. ${yours.price} {yours.currency}/{yours.billing_period} plus GST.
          </p>
        ) : (
          <p className="muted">Your tier is {me.tier_name}.</p>
        )}
        {plans.length === 0 ? (
          <div className="banner empty">No plans are saved yet.</div>
        ) : (
          <div className="tier-list">
            {plans.map((plan) => (
              <PlanOffer key={plan.name} plan={plan} />
            ))}
          </div>
        )}
      </MemberShell>
    );
  } catch (error) {
    const message = await handleMemberPageError(error);
    return (
      <MemberShell current="plan">
        <h1>Your plan</h1>
        <div className="banner error">{message}</div>
      </MemberShell>
    );
  }
}
