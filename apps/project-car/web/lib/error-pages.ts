// /member and /member/... go to the member dashboard. /members and /membership stay on /.
// Classify the path a browser would use. `/member/../schedule` is `/schedule`.
// `/members/../member/nope` is `/member/nope`. The parse base is not a request.
// window.location.pathname starts with one slash. A scheme, a relative string,
// or a protocol-relative prefix is not that pathname, so it stays on /.
// `/\evil.com\member\nope` is that prefix written with backslashes: the parser
// rewrites `\` to `/`, then the host is no longer the parse base.
export function dashboardHref(pathname: string): "/" | "/member" {
  if (!pathname.startsWith("/") || pathname.startsWith("//")) {
    return "/";
  }
  let path = "/";
  try {
    const url = new URL(pathname, "https://shop.invalid");
    if (url.host !== "shop.invalid") {
      return "/";
    }
    path = url.pathname;
  } catch {
    path = "/";
  }
  if (path === "/member" || path.startsWith("/member/")) {
    return "/member";
  }
  return "/";
}
