"use client";

import { useEffect, useState } from "react";

export function VisualProofShift() {
  const [shifted, setShifted] = useState(false);

  useEffect(() => {
    const timer = window.setTimeout(() => setShifted(true), 400);
    return () => window.clearTimeout(timer);
  }, []);

  if (!shifted) {
    return null;
  }

  return (
    <div
      data-visual-proof="shift"
      style={{
        height: 320,
        background: "#c45c4a",
        color: "#0b0c0e",
        fontWeight: 700,
        padding: "1rem 1.4rem",
      }}
    >
      Visual proof shift
    </div>
  );
}
