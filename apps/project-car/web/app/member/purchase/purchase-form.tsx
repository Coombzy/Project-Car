"use client";

import { useState } from "react";

import { buyTokensAction } from "./actions";

function gstPreview(subtotal: string): { gst: string; total: string } | null {
  if (!/^\d+(\.\d{1,2})?$/.test(subtotal)) {
    return null;
  }
  const [whole, fraction = ""] = subtotal.split(".");
  const cents = Number(whole) * 100 + Number(fraction.padEnd(2, "0"));
  if (!Number.isFinite(cents) || cents <= 0) {
    return null;
  }
  const gstCents = Math.round((cents * 5) / 100);
  const money = (value: number) => (value / 100).toFixed(2);
  return { gst: money(gstCents), total: money(cents + gstCents) };
}

export function PurchaseForm() {
  const [subtotal, setSubtotal] = useState("");
  const preview = gstPreview(subtotal);
  return (
    <form action={buyTokensAction} className="form-grid">
      <label>
        Payment id
        <input name="payment_id" placeholder="STANDIN-PAYPAL-WALK" autoComplete="off" />
      </label>
      <label>
        Tokens
        <input name="tokens" required inputMode="decimal" placeholder="200.00" />
      </label>
      <label>
        Before tax (CAD)
        <input
          name="subtotal_cad"
          required
          inputMode="decimal"
          placeholder="40.00"
          value={subtotal}
          onChange={(event) => setSubtotal(event.target.value)}
        />
      </label>
      <p>
        {preview
          ? `Subtotal $${subtotal} · GST $${preview.gst} · total $${preview.total}`
          : "GST is 5% of the before-tax amount. A blank payment id becomes a STANDIN id."}
      </p>
      <p className="muted">The stand-in payment adapter accepts STANDIN- ids until a processor is connected.</p>
      <div className="actions">
        <button type="submit">Buy tokens</button>
      </div>
    </form>
  );
}
