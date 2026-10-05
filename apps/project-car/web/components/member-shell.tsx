import type { ReactNode } from "react";
import { headers } from "next/headers";
import Link from "next/link";

import { memberLogoutAction } from "../app/member/logout-action";
import { memberShellCopy } from "../lib/member-shell-copy";
import { isCustomerShopHost } from "../lib/request-origin";

const NAV = [
  { href: "/member", current: "home", label: "Balance" },
  { href: "/member/schedule", current: "schedule", label: "Schedule" },
  { href: "/member/chat", current: "chat", label: "Chat" },
  { href: "/member/parts", current: "parts", label: "Parts" },
  { href: "/member/jobs", current: "jobs", label: "Job board" },
  { href: "/member/cameras", current: "cameras", label: "Cameras" },
] as const;

export type MemberSection = (typeof NAV)[number]["current"];

export async function MemberShell({
  email,
  current,
  wide,
  children,
}: {
  email?: string;
  current: MemberSection;
  wide?: boolean;
  children: ReactNode;
}) {
  const copy = memberShellCopy(isCustomerShopHost(await headers()));

  return (
    <div className="shell">
      <header className="topbar">
        <div className="brand">
          <strong>Project Car</strong>
          <span>{copy.subtitle}</span>
        </div>
        <nav className="nav">
          {NAV.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              aria-current={current === item.current ? "page" : undefined}
            >
              {item.label}
            </Link>
          ))}
          {email ? <span className="identity">{email}</span> : null}
          <form action={memberLogoutAction}>
            <button className="ghost" type="submit">
              Sign out
            </button>
          </form>
        </nav>
      </header>
      <div className="demo-banner">{copy.banner}</div>
      <main className={wide ? "wide" : undefined}>{children}</main>
    </div>
  );
}
