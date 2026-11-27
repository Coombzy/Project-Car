"use client";

import { MemberShell, type MemberSection } from "../../components/member-shell";

// A server error is not a nav section. Casting through string keeps every link unselected.
const NO_SECTION = ("missing" as string) as MemberSection;

export default function MemberError({
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <MemberShell current={NO_SECTION}>
      <h1>Something went wrong. Try again.</h1>
      <p className="actions">
        <button type="button" onClick={() => reset()}>Try again</button>
      </p>
    </MemberShell>
  );
}
