import fs from "node:fs";
import path from "node:path";

import { defineConfig } from "@playwright/test";

const webRoot = __dirname;
const fontsDir = path.join(webRoot, "visual", "fonts");
const shopNow = fs.readFileSync(path.join(webRoot, "visual", "shop-now.txt"), "utf8").trim();
const fontconfigPath = "/tmp/shop-web-visual-fonts.conf";

const sansFamilies = ["Segoe UI", "system-ui", "ui-sans-serif", "sans-serif"];
const monoFamilies = ["ui-monospace", "SF Mono", "Menlo", "monospace", "Courier New"];

function familyAssign(families: string[], resolved: string): string {
  return families
    .map(
      (family) => `  <match target="pattern">
    <test qual="any" name="family"><string>${family}</string></test>
    <edit name="family" mode="assign" binding="strong"><string>${resolved}</string></edit>
  </match>`,
    )
    .join("\n");
}

fs.writeFileSync(
  fontconfigPath,
  `<?xml version="1.0"?>
<fontconfig>
  <dir>${fontsDir}</dir>
  <cachedir>/tmp/shop-web-visual-fontcache</cachedir>
${familyAssign(sansFamilies, "Liberation Sans")}
${familyAssign(monoFamilies, "Liberation Mono")}
</fontconfig>
`,
);
process.env.FONTCONFIG_FILE = fontconfigPath;

const serverEnv = {
  SHOP_NOW: shopNow,
  NEXT_PUBLIC_SHOP_NOW: shopNow,
  SHOP_API_URL: "http://127.0.0.1:8000",
  FONTCONFIG_FILE: fontconfigPath,
};

export default defineConfig({
  testDir: "./visual",
  testMatch: "*.spec.ts",
  snapshotPathTemplate: "{testDir}/screenshots/{projectName}/{arg}{ext}",
  fullyParallel: false,
  workers: 1,
  forbidOnly: Boolean(process.env.CI),
  retries: 0,
  timeout: 60_000,
  reporter: process.env.CI ? [["github"], ["list"]] : "list",
  expect: {
    timeout: 15_000,
    toHaveScreenshot: {
      animations: "disabled",
      caret: "hide",
      scale: "css",
      maxDiffPixelRatio: 0.01,
    },
  },
  use: {
    baseURL: "http://127.0.0.1:3000",
    locale: "en-CA",
    timezoneId: "America/Regina",
    colorScheme: "dark",
    deviceScaleFactor: 1,
    reducedMotion: "reduce",
    launchOptions: {
      args: [
        "--font-render-hinting=none",
        "--disable-font-subpixel-positioning",
        "--disable-lcd-text",
        "--hide-scrollbars",
        "--force-color-profile=srgb",
      ],
    },
  },
  projects: [
    { name: "390", use: { viewport: { width: 390, height: 844 } } },
    { name: "768", use: { viewport: { width: 768, height: 1024 } } },
    { name: "1440", use: { viewport: { width: 1440, height: 900 } } },
  ],
  webServer: [
    {
      command: "bash visual/start-api.sh",
      url: "http://127.0.0.1:8000/health",
      timeout: 120_000,
      reuseExistingServer: false,
      env: {
        ...serverEnv,
        DATABASE_URL: "sqlite:////tmp/shop-visual.db",
        SHOP_HOST: "127.0.0.1",
      },
    },
    {
      command: "npx next start --port 3000",
      url: "http://127.0.0.1:3000/login",
      timeout: 120_000,
      reuseExistingServer: false,
      env: serverEnv,
    },
  ],
});
