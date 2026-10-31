// /member and /member/... go to the member dashboard. /members and /membership stay on /.
export function dashboardHref(pathname: string): "/" | "/member" {
  if (pathname === "/member" || pathname.startsWith("/member/")) {
    return "/member";
  }
  return "/";
}
