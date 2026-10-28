"use client";

import { OwnerShell, type OwnerSection } from "../components/owner-shell";

// A server error is not a nav section. Casting through string keeps every link unselected.
const NO_SECTION = ("missing" as string) as OwnerSection;

export default function ShopError({
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <OwnerShell current={NO_SECTION}>
      <h1>Something went wrong. Try again.</h1>
      <p className="actions">
        <button type="button" onClick={() => reset()}>Try again</button>
      </p>
    </OwnerShell>
  );
}
