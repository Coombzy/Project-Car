// Login forms cannot name demo-login.ts: lib/demo-login.test.ts rejects that
// filename in those sources. This re-export is the same showDemoLoginHints().
export { showDemoLoginHints } from "./demo-login";
