import assert from "node:assert/strict";
import { readdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join, relative } from "node:path";
import { describe, it } from "node:test";
import { fileURLToPath } from "node:url";

const webRoot = join(dirname(fileURLToPath(import.meta.url)), "..");
const css = readFileSync(join(webRoot, "app", "globals.css"), "utf8");

// Pinned from apps/website/html/styles.css (`--accent`, `--accent-warm`). That file has another owner.
const BROCHURE_PURPLE = "#c084fc";
const BROCHURE_ORANGE = "#e8a54b";

const TEXT = 4.5;
const NON_TEXT = 3;

type Rgba = { r: number; g: number; b: number; a: number };

function rootBlock(source: string): string {
  const match = source.match(/:root\s*\{([^}]*)\}/);
  assert.ok(match, "globals.css has no :root block");
  return match[1];
}

function rootTokens(source: string): Map<string, string> {
  const tokens = new Map<string, string>();
  for (const [, name, value] of rootBlock(source).matchAll(/--([\w-]+)\s*:\s*([^;]+);/g)) {
    tokens.set(name, value.trim());
  }
  return tokens;
}

const tokens = rootTokens(css);

function parseHex(value: string): Rgba | null {
  const match = value.match(/^#([0-9a-fA-F]{6})$/);
  if (!match) {
    return null;
  }
  const n = Number.parseInt(match[1], 16);
  return { r: (n >> 16) & 255, g: (n >> 8) & 255, b: n & 255, a: 1 };
}

function resolve(name: string, seen: string[] = []): Rgba {
  assert.ok(!seen.includes(name), `token cycle: ${[...seen, name].join(" -> ")}`);
  const value = tokens.get(name);
  assert.ok(value, `--${name} is not defined in :root`);
  const hex = parseHex(value);
  if (hex) {
    return hex;
  }
  const alias = value.match(/^var\(--([\w-]+)\)$/);
  if (alias) {
    return resolve(alias[1], [...seen, name]);
  }
  const wash = value.match(/^color-mix\(in srgb,\s*var\(--([\w-]+)\)\s+(\d+(?:\.\d+)?)%,\s*transparent\)$/);
  if (wash) {
    const base = resolve(wash[1], [...seen, name]);
    return { ...base, a: (base.a * Number(wash[2])) / 100 };
  }
  assert.fail(`--${name}: ${value} is not a hex, var() alias or color-mix() wash`);
}

function over(top: Rgba, under: Rgba): Rgba {
  return {
    r: top.r * top.a + under.r * (1 - top.a),
    g: top.g * top.a + under.g * (1 - top.a),
    b: top.b * top.a + under.b * (1 - top.a),
    a: 1,
  };
}

// "a over b" composites a translucent wash onto the surface it is painted on.
function backdrop(spec: string): Rgba {
  const layers = spec.split(" over ").map((name) => resolve(name));
  let colour = layers[layers.length - 1];
  assert.equal(colour.a, 1, `${spec}: the bottom layer must be opaque`);
  for (let i = layers.length - 2; i >= 0; i--) {
    colour = over(layers[i], colour);
  }
  return colour;
}

function luminance({ r, g, b }: Rgba): number {
  const channel = (c: number) => {
    const s = c / 255;
    return s <= 0.03928 ? s / 12.92 : ((s + 0.055) / 1.055) ** 2.4;
  };
  return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b);
}

function contrast(a: Rgba, b: Rgba): number {
  const [hi, lo] = [luminance(a), luminance(b)].sort((x, y) => y - x);
  return (hi + 0.05) / (lo + 0.05);
}

type Pair = { fg: string; bg: string; min: number };

const text = (fg: string, ...bgs: string[]): Pair[] => bgs.map((bg) => ({ fg, bg, min: TEXT }));
const edge = (fg: string, ...bgs: string[]): Pair[] => bgs.map((bg) => ({ fg, bg, min: NON_TEXT }));

const SURFACES = ["bg", "bg-glow", "surface-sunken", "surface", "surface-2"];

const PAIRS: Pair[] = [
  ...text("text", ...SURFACES, "purple-tint", "orange-tint", "info-tint", "danger-tint"),
  ...text("text", "purple-wash over surface", "orange-wash over surface", "danger-wash over surface"),
  ...text("text-muted", ...SURFACES, "orange-wash over surface", "orange-wash-soft over surface"),
  ...text("link", ...SURFACES),
  ...text("purple", "purple-tint"),
  ...text("orange", "surface", "orange-tint"),
  ...text("ok", "surface", "ok-tint"),
  ...text("warn", "surface", "warn-tint"),
  ...text("danger", "surface", "danger-tint"),
  ...text("info", "surface", "info-tint"),
  ...edge("border", ...SURFACES),
  ...edge("purple", ...SURFACES, "purple-tint"),
  ...edge("orange", ...SURFACES),
  ...edge("orange-line", "surface", "orange-tint"),
  ...edge("ok-line", "surface", "surface-sunken", "ok-tint"),
  ...edge("warn-line", "surface", "surface-sunken", "warn-tint"),
  ...edge("danger-line", "surface", "surface-sunken", "danger-tint"),
  ...edge("info-line", "surface", "surface-sunken", "info-tint"),
  ...edge("focus", ...SURFACES, "purple-tint"),
];

describe("shop theme tokens", () => {
  it("test_brand_tokens_match_the_brochure", () => {
    assert.equal(tokens.get("purple")?.toLowerCase(), BROCHURE_PURPLE);
    assert.equal(tokens.get("orange")?.toLowerCase(), BROCHURE_ORANGE);
  });

  it("test_token_pairs_meet_wcag_aa", () => {
    const failures: string[] = [];
    for (const { fg, bg, min } of PAIRS) {
      try {
        const ratio = contrast(over(resolve(fg), backdrop(bg)), backdrop(bg));
        if (ratio < min) {
          failures.push(`--${fg} on ${bg}: ${ratio.toFixed(2)} < ${min}`);
        }
      } catch (error) {
        failures.push(`--${fg} on ${bg}: ${(error as Error).message}`);
      }
    }
    assert.deepEqual(failures, []);
  });

  it("test_globals_css_colours_come_from_tokens", () => {
    const outsideRoot = css.replace(/:root\s*\{[^}]*\}/, "");
    const literals = [...outsideRoot.matchAll(/#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?)\(/g)].map((m) => m[0]);
    assert.deepEqual(literals, [], "colour literals outside :root");
  });

  it("test_old_tan_accent_is_gone", () => {
    const hits: string[] = [];
    const walk = (dir: string) => {
      for (const entry of readdirSync(dir)) {
        const path = join(dir, entry);
        if (statSync(path).isDirectory()) {
          walk(path);
        } else if (/\.(css|tsx?)$/.test(entry) && !entry.endsWith(".test.ts")) {
          const source = readFileSync(path, "utf8");
          if (/#c4a574|196,\s*165,\s*116/i.test(source)) {
            hits.push(relative(webRoot, path));
          }
        }
      }
    };
    for (const dir of ["app", "components", "lib"]) {
      walk(join(webRoot, dir));
    }
    assert.deepEqual(hits, []);
  });
});
