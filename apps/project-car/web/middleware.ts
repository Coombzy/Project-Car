import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

import { MEMBER_SESSION_COOKIE, SESSION_COOKIE } from "./lib/config";

export function middleware(request: NextRequest) {
  const path = request.nextUrl.pathname;
  const ownerSession = request.cookies.get(SESSION_COOKIE)?.value;
  const memberSession = request.cookies.get(MEMBER_SESSION_COOKIE)?.value;
  const isOwnerLogin = path.startsWith("/login");
  const isMemberLogin = path.startsWith("/member/login");
  const isMemberArea = path === "/member" || path.startsWith("/member/");

  if (isMemberLogin) {
    if (memberSession) {
      return NextResponse.redirect(new URL("/member", request.url));
    }
    return NextResponse.next();
  }

  if (isMemberArea) {
    if (!memberSession) {
      const login = new URL("/member/login", request.url);
      login.searchParams.set("next", path);
      return NextResponse.redirect(login);
    }
    return NextResponse.next();
  }

  if (!ownerSession && !isOwnerLogin) {
    const login = new URL("/login", request.url);
    login.searchParams.set("next", path);
    return NextResponse.redirect(login);
  }

  if (ownerSession && isOwnerLogin) {
    return NextResponse.redirect(new URL("/", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
