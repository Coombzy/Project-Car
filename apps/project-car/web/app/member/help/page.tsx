import { RateChart } from "../../../components/rate-chart";
import { MemberShell } from "../../../components/member-shell";
import { handleMemberPageError } from "../../../lib/page";
import { getMemberMe, getMemberRates } from "../../../lib/shop-api";

export const dynamic = "force-dynamic";

export default async function MemberHelpPage() {
  try {
    let me;
    try {
      me = await getMemberMe();
    } catch (error) {
      const message = await handleMemberPageError(error);
      return (
        <MemberShell current="help" wide>
          <h1>How rates work</h1>
          <div className="banner error">{message}</div>
        </MemberShell>
      );
    }
    const rates = await getMemberRates();
    return (
      <MemberShell email={me.email} current="help" wide>
        <p className="eyebrow">Rates · {rates.tz_label}</p>
        <h1>How rates work</h1>
        <p className="lede">
          A booking is priced one hour at a time. The colour of each hour is the band saved for the shop
          right now, in {rates.tz_label}.
        </p>
        <RateChart rates={rates} />
      </MemberShell>
    );
  } catch (error) {
    const message = await handleMemberPageError(error);
    return (
      <MemberShell current="help" wide>
        <h1>How rates work</h1>
        <div className="banner error">{message}</div>
      </MemberShell>
    );
  }
}
