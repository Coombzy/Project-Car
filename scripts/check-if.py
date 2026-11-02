#!/usr/bin/env python3
"""check-if.py: check a PR body's `IF:` merge-condition lines before you ask for merge.

Read-only. It only reads git, files and (optionally) `gh`. It mirrors the kinds the merge
checker understands, so an agent can see which lines will pass before review:

  IF: ci-green [check,check...]   every named check succeeded on the PR (needs gh). Bare = the merge
                                  guard's required checks for this repo (--required overrides)
  IF: red-green                   a commit whose message says RED (capitals), then a later commit
  IF: file-exists <path>          path exists at --ref (default HEAD)
  IF: file-absent <path>          path does not exist at --ref
  IF: file-contains <path> <text> file at --ref contains text
  IF: body-contains <text>        the PR body contains text

Usage:
  python3 scripts/check-if.py --body pr-body.md        # body from a file ('-' = stdin)
  python3 scripts/check-if.py --pr 123                 # body + checks from gh
  python3 scripts/check-if.py --self-test
Options: --ref REF (default HEAD), --base REF (default origin/main), --required a,b, --json.
A bad ref, unreadable git or gh error is "unverifiable", never "met".
Exit 0 = every line met, 1 = some line unmet/unverifiable or no IF: lines, 2 = usage error.
"""
import argparse, json, re, subprocess, sys

IF_LINE = re.compile(r"^\s*(?:[-*]\s+|\d+[.)]\s+)?`?IF:\s*([a-z-]+)\b[ \t]*(.*?)`?\s*$", re.M)
RED = re.compile(r"\bRED\b")
# Required checks per repo, as the merge guard uses them for a bare `IF: ci-green`.
REQUIRED = {"pbay": ["proof"],
            "project-car": ["shop-api pytest", "shop-web lint / typecheck / build", "shop-web layout-shift / screenshots"]}


class Unverifiable(Exception):
    pass


def git(*a, ok_codes=(0,)):
    r = subprocess.run(["git", *a], capture_output=True)
    if r.returncode not in ok_codes:
        raise Unverifiable(f"git {a[0]} failed: {r.stderr.decode(errors='replace').strip()[:120]}")
    return r


def repo_required():
    try:
        url = git("remote", "get-url", "origin").stdout.decode().strip().lower()
    except Unverifiable:
        return None
    for k in REQUIRED:
        if url.rstrip("/").removesuffix(".git").endswith("/" + k):
            return REQUIRED[k]
    return None


def parse(body):
    return [(m.group(1).lower(), m.group(2).strip()) for m in IF_LINE.finditer(body or "")]


class Ctx:
    def __init__(self, body, ref="HEAD", base="origin/main", pr=None, required=None):
        self.body, self.ref, self.base, self.pr, self.required = body, ref, base, pr, required

    def _spec(self, path):
        git("rev-parse", "--verify", "--quiet", f"{self.ref}^{{commit}}")  # bad ref / not a repo -> Unverifiable
        return f"{self.ref}:{path.removeprefix('./')}"

    def exists(self, path):
        return git("cat-file", "-e", self._spec(path), ok_codes=(0, 1, 128)).returncode == 0

    def file(self, path):
        """File text at ref (undecodable bytes replaced), or None when the path is not there."""
        if not self.exists(path):
            return None
        return git("show", self._spec(path)).stdout.decode(errors="replace")

    def checks(self):
        if not self.pr:
            raise RuntimeError("no --pr given, so CI checks are unknown")
        r = subprocess.run(["gh", "pr", "checks", str(self.pr), "--json", "name,bucket"], capture_output=True, text=True)
        try:  # gh exits 1 when a check failed and 8 when one is pending; the JSON is still on stdout
            data = json.loads(r.stdout)
        except ValueError:
            raise RuntimeError((r.stderr or "gh pr checks failed").strip()[:120])
        return {c["name"]: ("success" if c["bucket"] == "pass" else c["bucket"]) for c in data}

    def red_green(self):
        """Same rule as the merge guard: first commit whose message matches \\bRED\\b, and it is not the last."""
        out = git("log", "--reverse", "--format=%B%x00", f"{self.base}..{self.ref}").stdout.decode(errors="replace")
        msgs = [m for m in out.split("\0") if m.strip()]
        i = next((k for k, m in enumerate(msgs) if RED.search(m)), None)
        if i is None:
            return False, "no commit message says RED"
        if i == len(msgs) - 1:
            return False, "RED is the last commit (no GREEN after it)"
        return True, "RED commit, then a later commit"


def evaluate(kind, args, ctx):
    try:
        if kind == "ci-green":
            ch = ctx.checks()
            names = [n.strip() for n in args.split(",") if n.strip()] or ctx.required or list(ch)
            if not names:
                return "unmet", "no checks reported"
            bad = [f"{n}={ch.get(n, 'missing')}" for n in names if ch.get(n) != "success"]
            return ("unmet", "not green: " + ", ".join(bad)) if bad else ("met", "green: " + ", ".join(names))
        if kind == "red-green":
            ok, why = ctx.red_green()
            return ("met" if ok else "unmet"), why
        if kind in ("file-exists", "file-absent"):
            p = args.strip("`")
            ok = ctx.exists(p) == (kind == "file-exists")
            return ("met" if ok else "unmet"), p
        if kind == "file-contains":
            p, _, t = args.partition(" ")
            t = t.strip().strip("`\"'")
            got = ctx.file(p.strip("`"))
            if got is None:
                return "unmet", f"{p} missing"
            return ("met" if t and t in got else "unmet"), f"{p} {'has' if t in got else 'lacks'} {t[:40]!r}"
        if kind == "body-contains":
            t = args.strip("`\"'")
            return ("met" if t and t in (ctx.body or "") else "unmet"), t[:40]
    except Exception as e:  # report, never crash
        return "unverifiable", str(e)
    return "unverifiable", f"unknown IF kind {kind!r}"


def run(body, ctx):
    rows = [{"line": f"IF: {k} {a}".strip(), "kind": k, **dict(zip(("status", "why"), evaluate(k, a, ctx)))} for k, a in parse(body)]
    if not rows:
        rows.append({"line": "(none)", "kind": "parse", "status": "unmet", "why": "no IF: lines in the body; add e.g. 'IF: ci-green'"})
    return all(r["status"] == "met" for r in rows), rows


def self_test():
    import os, tempfile
    d = tempfile.mkdtemp()
    sh = lambda *a: subprocess.run(["git", "-C", d, *a], check=True, capture_output=True)
    sh("init", "-q", "-b", "main"); sh("config", "user.email", "t@t"); sh("config", "user.name", "t")
    open(f"{d}/app.py", "w").write("x = 1\n"); open(f"{d}/logo.png", "wb").write(b"\x89PNG\xff\xfe")
    sh("add", "."); sh("commit", "-qm", "base"); sh("branch", "base")
    os.makedirs(f"{d}/tests"); open(f"{d}/tests/test_app.py", "w").write("assert 0\n"); sh("add", "."); sh("commit", "-qm", "RED: failing test")
    open(f"{d}/app.py", "w").write("x = 2  # fixed\n"); sh("add", "."); sh("commit", "-qm", "GREEN: fix")
    sh("branch", "redlast", "HEAD~1"); sh("checkout", "-qb", "lower", "base")
    os.makedirs(f"{d}/tests", exist_ok=True); open(f"{d}/tests/t1.py", "w").write("1\n"); sh("add", "."); sh("commit", "-qm", "red")
    open(f"{d}/tests/t2.py", "w").write("2\n"); sh("add", "."); sh("commit", "-qm", "more tests"); sh("checkout", "-q", "main")
    cwd = os.getcwd(); os.chdir(d)
    try:
        body = "Fix x\n\n## Merge conditions\nIF: file-exists logo.png\n- IF: file-exists app.py\n- `IF: file-contains app.py fixed`\nIF: file-absent nope.txt\nIF: file-exists ./app.py\nIF: red-green\nIF: body-contains Fix x\n"
        ok, rows = run(body, Ctx(body, base="base"))
        assert ok and len(rows) == 7, rows
        ok, rows = run("IF: file-contains app.py nothere\nIF: bogus\nIF: ci-green", Ctx("", base="base"))
        assert not ok and [r["status"] for r in rows] == ["unmet", "unverifiable", "unverifiable"], rows
        assert not run("no conditions", Ctx(""))[0]
        assert not run("IF: red-green", Ctx("", base="HEAD~1"))[0]  # only the GREEN commit in range
        assert not run("IF: red-green", Ctx("", ref="redlast", base="base"))[0]  # RED is last
        assert not run("IF: red-green", Ctx("", ref="lower", base="base"))[0]  # lowercase "red" is not RED
        for k in ("file-absent nope.txt", "file-exists app.py"):  # bad ref is unverifiable, never met
            assert evaluate(*k.split(" ", 1), Ctx("", ref="no-such-ref"))[0] == "unverifiable", k
        c = Ctx(""); c.checks = lambda: {"a": "success", "b": "fail"}
        assert evaluate("ci-green", "a", c)[0] == "met" and evaluate("ci-green", "", c)[0] == "unmet"
        assert evaluate("ci-green", "b", c)[0] == "unmet"
        c.required = ["proof"]; c.checks = lambda: {"lint": "success"}
        assert evaluate("ci-green", "", c)[0] == "unmet"  # bare = required list, proof missing
    finally:
        os.chdir(cwd)
    e = tempfile.mkdtemp(); os.chdir(e)  # outside any repo: file-absent must not be met
    try:
        assert evaluate("file-absent", "nope.txt", Ctx(""))[0] == "unverifiable"
    finally:
        os.chdir(cwd)
    print("check-if selftest ok")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--body"); ap.add_argument("--pr"); ap.add_argument("--ref", default="HEAD")
    ap.add_argument("--base", default="origin/main"); ap.add_argument("--json", action="store_true"); ap.add_argument("--required")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if a.body:
        body = sys.stdin.read() if a.body == "-" else open(a.body).read()
    elif a.pr:
        r = subprocess.run(["gh", "pr", "view", a.pr, "--json", "body", "-q", ".body"], capture_output=True, text=True)
        if r.returncode:
            sys.exit(f"check-if: gh pr view failed: {r.stderr.strip()[:200]}")
        body = r.stdout
    else:
        ap.print_usage(); sys.exit(2)
    req = [x.strip() for x in a.required.split(",") if x.strip()] if a.required else repo_required()
    ok, rows = run(body, Ctx(body, a.ref, a.base, a.pr, req))
    if a.json:
        print(json.dumps({"ok": ok, "rows": rows}, indent=1))
    else:
        for r in rows:
            print(f"[{r['status']}] {r['line']}  ({r['why']})")
        print("check-if: all met" if ok else "check-if: NOT all met")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
