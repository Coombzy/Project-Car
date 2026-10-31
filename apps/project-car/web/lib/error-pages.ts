// /member and /member/... go to the member dashboard. /members and /membership stay on /.
// Classify the path a browser would use. `/member/../schedule` is `/schedule`.
// `/members/../member/nope` is `/member/nope`. The parse base is not a request.
export function dashboardHref(pathname: string): "/" | "/member" {
  let path = pathname;
  try {
    path = new URL(pathname, "https://shop.invalid").pathname;
  } catch {
    path = "/";
  }
  if (path === "/member" || path.startsWith("/member/")) {
    return "/member";
  }
  return "/";
}
