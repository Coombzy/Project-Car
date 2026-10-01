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
          · ops.projectcar.ca LIVE · app. alias · shop not open · not live pricing, Stripe, or
          camera feeds
        </span>
      </p>
      <details className="demo-banner-more">
        <summary>Details</summary>
        <p>
          Management demo on ops.projectcar.ca (LIVE at the edge when Doc is up). app.projectcar.ca
          is the temporary alias for the same Doc shop UI. Calendar is the month heat-map + weekly
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
