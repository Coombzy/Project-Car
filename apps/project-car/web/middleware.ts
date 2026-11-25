import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

import { MEMBER_SESSION_COOKIE, SESSION_COOKIE } from "./lib/config";
import {
  CUSTOMER_HOST_OPS_LOGIN,
  customerHostAllowsPath,
  isCustomerShopHost,
  publicUrl,
} from "./lib/request-origin";
import { applySecurityHeaders } from "./lib/security-headers";

function redirectTo(request: NextRequest, path: string): URL {
  return publicUrl(request.headers, request.url, path);
}

/** Shape only. Empty, whitespace, spaces, and ASCII controls fail. Not a signature check. */
function cookieLooksPlausible(value: string): boolean {
  if (value.trim() === "") return false;
  for (let index = 0; index < value.length; index += 1) {
    const code = value.charCodeAt(index);
    if (code <= 0x20 || code === 0x7f) return false;
  }
  return true;
}

function redirect(url: string | URL): NextResponse {
  return applySecurityHeaders(NextResponse.redirect(url));
}

const PUBLIC_INSTALL_PATHS = new Set(["/manifest.webmanifest"]);

export function middleware(request: NextRequest) {
  const path = request.nextUrl.pathname;

  // Browsers request the web manifest without a session cookie.
  if (PUBLIC_INSTALL_PATHS.has(path)) {
    return NextResponse.next();
  }

  // Customer host is Member-only. Do this before owner-login redirects so
  // `/` and `/login` never render on projectcar.ca / www.
  if (isCustomerShopHost(request.headers) && !customerHostAllowsPath(path)) {
    return redirect(CUSTOMER_HOST_OPS_LOGIN);
  }

  const ownerSession = request.cookies.get(SESSION_COOKIE)?.value;
  const memberSession = request.cookies.get(MEMBER_SESSION_COOKIE)?.value;
  const isOwnerLogin = path.startsWith("/login");
  const isMemberLogin = path.startsWith("/member/login");
  const isSignup = path === "/signup" || path.startsWith("/signup/");
  const isMemberArea = path === "/member" || path.startsWith("/member/");
  const ownerExpired = "/logout/expired";
  const memberExpired = "/member/logout/expired";
  if (isMemberArea && path !== memberExpired && memberSession && !cookieLooksPlausible(memberSession)) {
    return redirect(redirectTo(request, memberExpired));
  }
  if (!isMemberArea && !isSignup && path !== ownerExpired && ownerSession && !cookieLooksPlausible(ownerSession)) {
    return redirect(redirectTo(request, ownerExpired));
  }
  if (path === ownerExpired || path === memberExpired) return NextResponse.next();

  if (isMemberLogin) {
    if (memberSession) {
      return redirect(redirectTo(request, "/member"));
    }
    return NextResponse.next();
  }

  if (isSignup) {
    return NextResponse.next();
  }

  if (isMemberArea) {
    if (!memberSession) {
      const login = redirectTo(request, "/member/login");
      login.searchParams.set("next", path);
      return redirect(login);
    }
    return NextResponse.next();
  }

  if (!ownerSession && !isOwnerLogin) {
    const login = redirectTo(request, "/login");
    login.searchParams.set("next", path);
    return redirect(login);
  }

  if (ownerSession && isOwnerLogin) {
    return redirect(redirectTo(request, "/"));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico|manifest\\.webmanifest).*)"],
};
