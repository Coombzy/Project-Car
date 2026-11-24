import {readFileSync as r} from "node:fs";
import {test} from "node:test";
import assert from "node:assert/strict";
test("SHOP_DEV_MODE",()=>{
  assert.match(r(new URL("./start-api.sh",import.meta.url),"utf8"),/export SHOP_DEV_MODE="\$\{SHOP_DEV_MODE:-1\}"|export SHOP_DEV_MODE=1\b/);
  const c=r(new URL("../playwright.config.ts",import.meta.url),"utf8"),a=c.indexOf("bash visual/start-api.sh"),b=c.slice(Math.max(0,a)),n=b.indexOf("npx next start");
  assert.ok(a>=0,"API webServer command missing");
  assert.match(n<0?b:b.slice(0,n),/SHOP_DEV_MODE:\s*"1"/);
});
