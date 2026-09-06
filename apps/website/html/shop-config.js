/* Project Car public shop API base.
 * Override before this file loads: window.PC_SHOP_API_BASE = "https://...";
 * Or edit the default below for a deploy. Do not hardcode localhost in production HTML.
 */
(function (w) {
  var DEFAULT_BASE = "https://api.projectcar.ca";
  w.PC_SHOP_API_BASE = (typeof w.PC_SHOP_API_BASE === "string" && w.PC_SHOP_API_BASE.trim())
    ? w.PC_SHOP_API_BASE.trim().replace(/\/$/, "")
    : DEFAULT_BASE;
})(window);
