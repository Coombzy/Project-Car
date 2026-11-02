#!/usr/bin/env python3
"""related-tests.py: map changed files to the tests that cover them (vendored from the box's related_tests.py; keep in sync).
  python3 scripts/related-tests.py [--run] [file ...]     default files: git diff --name-only origin/main...HEAD + worktree
Prints one `cd <dir> && <cmd>` line per command. --run executes them and exits non-zero on the first failure.
A file with no mapped test falls back to that area's full command, never "no tests". scripts/pr-ready.sh still runs
the full set before a PR."""
import glob, os, re, sys
API, WEB = "apps/project-car/api", "apps/project-car/web"
API_FULL = (API, "python -m pytest -q -o addopts= -p no:cacheprovider")
WEB_FULL = (WEB, "node --experimental-strip-types --test lib/*.test.ts")
DOC = re.compile(r"\.(md|txt|png|jpg|svg|css)$|^Docs/|(^|/)README", re.I)

def _rd(p):
    try: return open(p, errors="replace").read()
    except OSError: return ""

def api_tests(tree, f):
    rel = f[len(API) + 1:]
    if re.match(r"tests/(test_[^/]+|conftest)\.py$", rel):
        return None if rel.endswith("conftest.py") else [rel]
    if not rel.endswith(".py"): return None
    stem, mod = os.path.basename(rel)[:-3], rel[:-3].replace("/", ".")
    out = sorted({os.path.relpath(p, f"{tree}/{API}") for p in glob.glob(f"{tree}/{API}/tests/test_{stem}*.py")})
    pat = re.compile(rf"(from|import)\s+{re.escape(mod)}\b|from\s+{re.escape(mod.rsplit('.', 1)[0])}\s+import\s+[^\n]*\b{re.escape(stem)}\b")
    out += sorted(os.path.relpath(p, f"{tree}/{API}") for p in glob.glob(f"{tree}/{API}/tests/test_*.py")
                  if pat.search(_rd(p)) and os.path.relpath(p, f"{tree}/{API}") not in out)
    return out or None

def web_tests(tree, f):
    rel = f[len(WEB) + 1:]
    if re.search(r"\.test\.tsx?$", rel): return [rel]
    if not re.search(r"\.(ts|tsx|js|mjs)$", rel): return []   # css/assets/json: typecheck/build is the box's job
    stem = re.sub(r"\.(ts|tsx|js|mjs)$", "", os.path.basename(rel))
    out = [os.path.relpath(p, f"{tree}/{WEB}") for p in glob.glob(f"{tree}/{WEB}/{os.path.dirname(rel)}/{stem}.test.ts*")]
    pat = re.compile(rf"""from\s+['"][^'"]*/{re.escape(stem)}(\.tsx?)?['"]""")
    out += [os.path.relpath(p, f"{tree}/{WEB}") for p in sorted(glob.glob(f"{tree}/{WEB}/lib/*.test.ts")) if pat.search(_rd(p)) and os.path.relpath(p, f"{tree}/{WEB}") not in out]
    return out or None

def plan(tree, files):
    """-> list of (cwd, command, why). Empty list = nothing to run (docs only)."""
    files = [f.strip() for f in files if f.strip()]
    if not files:   # no allowed-files list -> cannot map; run the full set for the repo
        if os.path.isdir(f"{tree}/apps/project-car"): return [API_FULL + ("full",), (WEB, "npm run -s typecheck", "full"), WEB_FULL + ("full",)], ["no changed-file list -> full suite"]
        if os.path.isfile(f"{tree}/package.json"): return [(".", "npm run -s v0-proof", "full"), (".", "npm run -s contract-proof", "full")], ["no changed-file list -> full proofs"]
        return [], ["no changed-file list and no known test layout"]
    api, web, api_full, web_full, tc, pbay, why = set(), set(), False, False, False, set(), []
    is_pbay = os.path.isfile(f"{tree}/package.json") and not os.path.isdir(f"{tree}/apps/project-car")
    for f in files:
        if f.startswith(API + "/"):
            t = api_tests(tree, f)
            if t is None: api_full = True; why.append(f"{f}: no mapped test -> full api pytest")
            else: api |= set(t)
        elif f.startswith(WEB + "/"):
            t = web_tests(tree, f); tc |= bool(re.search(r"\.tsx?$", f))
            if t is None: web_full = True; why.append(f"{f}: no mapped test -> all web unit tests")
            else: web |= set(t)
        elif is_pbay and not DOC.search(f):
            stem = re.sub(r"\.\w+$", "", os.path.basename(f)); hit = False
            for s in ("v0-proof", "contract-proof"):
                src = _rd(f"{tree}/scripts/{s}.ts")
                if f == f"scripts/{s}.ts" or (stem and re.search(rf"""['"][^'"]*\b{re.escape(stem)}(\.ts)?['"]""", src)): pbay.add(s); hit = True
            if not hit: pbay |= {"v0-proof", "contract-proof"}; why.append(f"{f}: no proof imports it -> both proofs")
        elif not DOC.search(f) and not is_pbay and not f.startswith(("apps/project-car/", "Docs/")):
            why.append(f"{f}: outside a known test area")
    out = []
    if api_full: out.append(API_FULL + ("full",))
    elif api: out.append((API, f"python -m pytest -q -o addopts= -p no:cacheprovider {' '.join(sorted(api))}", "related"))
    if tc: out.append((WEB, "npm run -s typecheck", "ts changed"))
    if web_full: out.append(WEB_FULL + ("full",))
    elif web: out.append((WEB, f"node --experimental-strip-types --test {' '.join(sorted(web))}", "related"))
    for s in sorted(pbay): out.append((".", f"npm run -s {s}", "proof"))
    return out, why


def changed(tree):
    import subprocess
    def g(*a):
        r = subprocess.run(["git", "-C", tree, *a], capture_output=True, text=True)
        return r.stdout.split() if r.returncode == 0 else []
    base = "origin/main" if g("rev-parse", "--verify", "-q", "origin/main") else "main"
    fs = set(g("diff", "--name-only", f"{base}...HEAD")) | set(g("diff", "--name-only", "HEAD")) | set(g("ls-files", "--others", "--exclude-standard"))
    return sorted(fs)

def main(argv):
    import subprocess
    run = "--run" in argv; files = [a for a in argv if a != "--run"]
    tree = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    files = files or changed(tree)
    cmds, why = plan(tree, files)
    for w in why: print(f"# {w}")
    if not cmds: print("# nothing to run: docs/assets only"); return 0
    import shutil
    py = "python" if shutil.which("python") else "python3"
    for cwd, cmd, _ in cmds:
        if cmd.startswith("python "): cmd = py + cmd[6:]
        print(f"cd {cwd} && {cmd}")
        if run:
            rc = subprocess.run(cmd, shell=True, cwd=os.path.join(tree, cwd)).returncode
            if rc: print(f"# FAILED rc={rc}: {cmd}"); return rc
    return 0

if __name__ == "__main__": sys.exit(main(sys.argv[1:]))
