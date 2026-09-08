"use client";

import { useEffect, useState } from "react";

const STORAGE_KEY = "pc-owner-demo-banner-dismissed";

export function OwnerDemoBanner() {
  const [dismissed, setDismissed] = useState(false);

  useEffect(() => {
    try {
      setDismissed(sessionStorage.getItem(STORAGE_KEY) === "1");
    } catch {
      setDismissed(false);
    }
  }, []);

  if (dismissed) {
    return null;
  }

  function dismiss() {
    try {
      sessionStorage.setItem(STORAGE_KEY, "1");
    } catch {
      /* ignore quota / private mode */
    }
    setDismissed(true);
  }

  return (
    <div className="demo-banner compact">
      <p className="demo-banner-line">
        <strong>Demo</strong>
        <span>
          {" "}
          · app.projectcar.ca alias · shop not open · not live pricing, Stripe, or camera feeds
        </span>
      </p>
      <details className="demo-banner-more">
        <summary>Details</summary>
        <p>
          Management demo on the current app.projectcar.ca alias (Doc). Intended host is
          ops.projectcar.ca — naming only, no DNS yet. Calendar is the month heat-map + weekly
          per-hoist grids. Dashboard is Bays 1–6 next 24h, personal to-dos, and current parts POs.
          Parts (PT) and Tools (B1–B6 bay kits + TC crib) use locked SKU prefixes — labeled
          placeholders, not live purchasing, checkout, or camera feeds. The shop is not open. This
          is not live pricing or Stripe.
        </p>
      </details>
      <button className="ghost demo-banner-dismiss" type="button" onClick={dismiss}>
        Dismiss
      </button>
    </div>
  );
}
