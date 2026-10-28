"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

import { OwnerShell, type OwnerSection } from "../components/owner-shell";

// A missing page is not a nav section. Casting through string keeps every link unselected.
const NO_SECTION = ("missing" as string) as OwnerSection;

// Unmatched URLs are rendered as the static /_not-found route, so usePathname()
// is "/_not-found" and cannot tell /member/... from an owner URL.
function dashboardHref(pathname: string): "/" | "/member" {
  if (pathname === "/member" || pathname.startsWith("/member/")) {
    return "/member";
  }
  return "/";
}

export default function NotFound() {
  const [pathname, setPathname] = useState("");
  useEffect(() => {
    setPathname(window.location.pathname);
  }, []);

  return (
    <OwnerShell current={NO_SECTION}>
      <h1>That page is not here.</h1>
      <p className="lede">
        <Link href={dashboardHref(pathname)}>Dashboard</Link>
      </p>
    </OwnerShell>
  );
}
