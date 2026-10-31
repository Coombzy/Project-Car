import type { MembershipTier } from "../lib/config";

export function PlanOffer({
  plan,
  framed = true,
}: {
  plan: MembershipTier;
  framed?: boolean;
}) {
  const body = (
    <>
      {framed ? <h2>{plan.display_name}</h2> : null}
      {plan.price_mark ? <p className="banner">{plan.price_mark}</p> : null}
      <p>
        <strong>
          ${plan.price} {plan.currency}/{plan.billing_period}
        </strong>{" "}
        plus GST
      </p>
      <p className="muted">
        GST ${plan.gst_cad} · ${plan.total_cad} {plan.currency} with GST
      </p>
      <p className="muted">{plan.included_tokens} tokens included this period</p>
      {framed && plan.notes ? <p className="muted">{plan.notes}</p> : null}
    </>
  );
  if (!framed) {
    return <div className="plan-offer">{body}</div>;
  }
  return <article className="card plan-offer">{body}</article>;
}
