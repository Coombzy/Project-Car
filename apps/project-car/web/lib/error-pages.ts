// /member and /member/... go to the member dashboard. /members and /membership stay on /.
// Classify the path a browser would use. `/member/../schedule` is `/schedule`.
// `/members/../member/nope` is `/member/nope`. The parse base is not a request.
// window.location.pathname starts with one slash. A scheme, a relative string,
// or a protocol-relative prefix is not that pathname, so it stays on /.
// A raw `\` is not that pathname. new URL rewrites `\` to `/`, so
// `/\shop.invalid\member\nope` stays on the parse base and the host check
// would return /member. Reject `\` before new URL.
// A raw control is not that pathname either. The parser deletes it, so
// `/member\t/nope` would otherwise look like `/member/nope`.
export function dashboardHref(pathname: string): "/" | "/member" {
  if (!pathname.startsWith("/") || pathname.startsWith("//")) {
    return "/";
  }
  if (pathname.includes("\\") || /[\u0000-\u001F\u007F]/.test(pathname)) {
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
