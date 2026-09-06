import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

import { MEMBER_SESSION_COOKIE, SESSION_COOKIE } from "./lib/config";
import { publicUrl } from "./lib/request-origin";

function redirectTo(request: NextRequest, path: string): URL {
  return publicUrl(request.headers, request.url, path);
}

export function middleware(request: NextRequest) {
  const path = request.nextUrl.pathname;
  const ownerSession = request.cookies.get(SESSION_COOKIE)?.value;
  const memberSession = request.cookies.get(MEMBER_SESSION_COOKIE)?.value;
  const isOwnerLogin = path.startsWith("/login");
  const isMemberLogin = path.startsWith("/member/login");
  const isMemberArea = path === "/member" || path.startsWith("/member/");

  if (isMemberLogin) {
    if (memberSession) {
      return NextResponse.redirect(redirectTo(request, "/member"));
    }
    return NextResponse.next();
  }

  if (isMemberArea) {
    if (!memberSession) {
      const login = redirectTo(request, "/member/login");
      login.searchParams.set("next", path);
      return NextResponse.redirect(login);
    }
    return NextResponse.next();
  }

  if (!ownerSession && !isOwnerLogin) {
    const login = redirectTo(request, "/login");
    login.searchParams.set("next", path);
    return NextResponse.redirect(login);
  }

  if (ownerSession && isOwnerLogin) {
    return NextResponse.redirect(redirectTo(request, "/"));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
