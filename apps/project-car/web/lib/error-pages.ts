// /member and /member/... go to the member dashboard. /members and /membership stay on /.
// Classify the path a browser would use. `/member/../schedule` is `/schedule`.
// `/members/../member/nope` is `/member/nope`. The parse base is not a request.
// window.location.pathname starts with one slash. A scheme, a relative string,
// or a protocol-relative prefix is not that pathname, so it stays on /.
export function dashboardHref(pathname: string): "/" | "/member" {
  if (!pathname.startsWith("/") || pathname.startsWith("//")) {
    return "/";
  }
  let path = "/";
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
