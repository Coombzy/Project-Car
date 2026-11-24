"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

import { MemberShell, type MemberSection } from "../components/member-shell";
import { OwnerShell, type OwnerSection } from "../components/owner-shell";
import { dashboardHref } from "../lib/error-pages";

// A missing page is not a nav section. Casting through string keeps every link unselected.
const NO_SECTION = ("missing" as string) as OwnerSection;
const NO_MEMBER_SECTION = ("missing" as string) as MemberSection;

// Unmatched URLs are rendered as the static /_not-found route, so usePathname()
// is "/_not-found" and cannot tell /member/... from an owner URL.

export default function NotFound() {
  // Null until the effect stores window.location.pathname. An empty string is
  // still a string, so the first render would ship Dashboard href="/" for /member/...
  const [pathname, setPathname] = useState<string | null>(null);
  useEffect(() => {
    setPathname(window.location.pathname);
  }, []);

  const page = (
    <>
      <h1>That page is not here.</h1>
      {typeof pathname === "string" ? (
        <p className="lede">
          <Link href={dashboardHref(pathname)}>Dashboard</Link>
        </p>
      ) : null}
    </>
  );

  if (typeof pathname === "string" && dashboardHref(pathname) === "/member") {
    return <MemberShell current={NO_MEMBER_SECTION}>{page}</MemberShell>;
  }

  return <OwnerShell current={NO_SECTION}>{page}</OwnerShell>;
}
