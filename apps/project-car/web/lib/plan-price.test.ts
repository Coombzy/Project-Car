import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { describe, it } from "node:test";

const sources = {
  signup: readFileSync(new URL("../app/member/login/page.tsx", import.meta.url), "utf8"),
  waitlist: readFileSync(new URL("../app/waitlist/page.tsx", import.meta.url), "utf8"),
  plan: readFileSync(new URL("../app/tiers/page.tsx", import.meta.url), "utf8"),
  memberPlan: readFileSync(new URL("../app/member/plan/page.tsx", import.meta.url), "utf8"),
  offer: readFileSync(new URL("../components/plan-offer.tsx", import.meta.url), "utf8"),
};

describe("plan price screens", () => {
  it("renders the saved CAD price plus GST and the premium stand-in mark", () => {
    for (const source of [sources.signup, sources.waitlist, sources.plan, sources.memberPlan]) {
      assert.match(source, /PlanOffer/);
      assert.doesNotMatch(source, /\$500|\$750|500\.00|750\.00/);
    }
    assert.match(sources.offer, /price_mark/);
    assert.match(sources.offer, /gst_cad/);
    assert.match(sources.offer, /plus GST/);
    assert.doesNotMatch(sources.offer, /500|750/);
    assert.match(sources.signup, /listPublicPlans/);
    assert.match(sources.memberPlan, /listPublicPlans/);
  });
});
