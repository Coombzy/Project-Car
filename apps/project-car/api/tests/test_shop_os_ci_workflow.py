from __future__ import annotations

import os
import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
WORKFLOW = ROOT / ".github" / "workflows" / "shop-os-ci.yml"
PAGES = ROOT / "apps" / "project-car" / "web" / "visual" / "pages.spec.ts"
PLAYWRIGHT = ROOT / "apps" / "project-car" / "web" / "playwright.config.ts"
RUNBOOK = ROOT / "Docs" / "shop-os-ci.md"
PACKAGE = ROOT / "apps" / "project-car" / "web" / "package.json"

REQUIRED_CHECK_NAMES = (
    "shop-api pytest",
    "shop-web lint / typecheck / build",
)
VISUAL_CHECK_NAME = "shop-web layout-shift / screenshots"
HEAVY_COMMANDS = {
    "shop-api pytest": ("pytest",),
    "shop-web lint / typecheck / build": ("npm run typecheck", "npm test", "npm run build"),
    "shop-web layout-shift / screenshots": ("npm run visual",),
}
GATE_IF = "steps.shop_changes.outputs.shop == 'true'"
BASELINE_PREPARE_IF = (
    "steps.shop_changes.outputs.shop == 'true' && "
    "github.event_name == 'push' && github.ref == 'refs/heads/main'"
)
BASELINE_STORE_IF = (
    "steps.shop_changes.outputs.shop == 'true' && "
    "github.event_name == 'push' && github.ref == 'refs/heads/main' && "
    "steps.screenshot_baselines.outputs.cache-hit != 'true'"
)
PUSH_GUARD = 'if [ "${GITHUB_EVENT_NAME}" = "push" ]; then'
DIFF_COMMAND = 'git diff --name-only --no-renames "${base}" HEAD'


def _strip_comment(line: str) -> str:
    in_single = False
    in_double = False
    escaped = False
    for index, char in enumerate(line):
        if escaped:
            escaped = False
            continue
        if char == "\\" and (in_single or in_double):
            escaped = True
            continue
        if char == "'" and not in_double:
            in_single = not in_single
            continue
        if char == '"' and not in_single:
            in_double = not in_double
            continue
        if char == "#" and not in_single and not in_double:
            return line[:index]
    return line


def _parse_scalar(raw: str):
    value = raw.strip()
    if value == "" or value in {"null", "~", "Null", "NULL"}:
        return None
    if value in {"true", "True", "TRUE"}:
        return True
    if value in {"false", "False", "FALSE"}:
        return False
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if inner == "":
            return []
        return [_parse_scalar(part.strip()) for part in inner.split(",")]
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def _split_key(content: str) -> tuple[str, str]:
    key, separator, rest = content.partition(":")
    if separator != ":":
        raise ValueError(f"expected a YAML key, got {content!r}")
    return key.strip(), rest.strip()


class _WorkflowYaml:
    """Parse the mapping, list, and literal-block subset used by shop-os-ci.yml.

    GitHub Actions keeps the key `on` as a string. A YAML 1.1 bool schema would
    turn that key into True, so this parser does not.
    """

    def __init__(self, text: str) -> None:
        self.lines = text.splitlines()
        self.index = 0

    def parse(self) -> dict:
        document = self._parse_map(0)
        self._skip_noise()
        if self.index != len(self.lines):
            raw = self.lines[self.index]
            raise ValueError(f"trailing workflow content at line {self.index + 1}: {raw!r}")
        return document

    def _skip_noise(self) -> None:
        while self.index < len(self.lines):
            raw = self.lines[self.index]
            stripped = raw.strip()
            if stripped == "" or stripped.startswith("#"):
                self.index += 1
                continue
            return

    def _peek(self) -> tuple[int, str] | None:
        self._skip_noise()
        if self.index >= len(self.lines):
            return None
        stripped = _strip_comment(self.lines[self.index]).rstrip()
        if stripped.strip() == "":
            self.index += 1
            return self._peek()
        indent = len(stripped) - len(stripped.lstrip(" "))
        return indent, stripped.lstrip(" ")

    def _parse_map(self, indent: int) -> dict:
        mapping: dict = {}
        while True:
            peeked = self._peek()
            if peeked is None or peeked[0] < indent:
                break
            line_indent, content = peeked
            if line_indent != indent or content.startswith("- "):
                raise ValueError(f"expected a mapping key at indent {indent}, got {content!r}")
            self.index += 1
            key, rest = _split_key(content)
            mapping[key] = self._parse_value(line_indent, rest)
        return mapping

    def _parse_list(self, indent: int) -> list:
        items: list = []
        while True:
            peeked = self._peek()
            if peeked is None or peeked[0] < indent:
                break
            line_indent, content = peeked
            if line_indent != indent or not content.startswith("- "):
                break
            self.index += 1
            item_body = content[2:]
            if item_body == "":
                child = self._peek()
                if child is None or child[0] <= line_indent:
                    items.append(None)
                elif child[1].startswith("- "):
                    items.append(self._parse_list(child[0]))
                else:
                    items.append(self._parse_map(child[0]))
                continue
            _key, separator, _rest = item_body.partition(":")
            if separator == ":":
                items.append(self._parse_list_item(line_indent, item_body))
            else:
                items.append(_parse_scalar(item_body))
        return items

    def _parse_list_item(self, dash_indent: int, first: str) -> dict:
        item: dict = {}
        key, rest = _split_key(first)
        item[key] = self._parse_value(dash_indent, rest)
        while True:
            peeked = self._peek()
            if peeked is None or peeked[0] <= dash_indent or peeked[1].startswith("- "):
                break
            line_indent, content = peeked
            self.index += 1
            child_key, child_rest = _split_key(content)
            item[child_key] = self._parse_value(line_indent, child_rest)
        return item

    def _parse_value(self, key_indent: int, rest: str):
        if rest in {"|", "|-", "|+"}:
            return self._parse_literal(key_indent)
        if rest != "":
            return _parse_scalar(rest)
        peeked = self._peek()
        if peeked is None or peeked[0] <= key_indent:
            return None
        child_indent, child = peeked
        if child.startswith("- "):
            return self._parse_list(child_indent)
        return self._parse_map(child_indent)

    def _parse_literal(self, key_indent: int) -> str:
        block_indent: int | None = None
        chunks: list[str] = []
        while self.index < len(self.lines):
            raw = self.lines[self.index]
            if raw.strip() == "":
                chunks.append("")
                self.index += 1
                continue
            indent = len(raw) - len(raw.lstrip(" "))
            if indent <= key_indent:
                break
            if block_indent is None:
                block_indent = indent
            if indent < block_indent:
                break
            chunks.append(raw[block_indent:])
            self.index += 1
        while chunks and chunks[-1] == "":
            chunks.pop()
        return "\n".join(chunks)


def parse_workflow_yaml(text: str) -> dict:
    return _WorkflowYaml(text).parse()


def _contains_key(node: object, key: str) -> bool:
    if isinstance(node, dict):
        if key in node:
            return True
        return any(_contains_key(value, key) for value in node.values())
    if isinstance(node, list):
        return any(_contains_key(item, key) for item in node)
    return False


def _detect_script(workflow: dict, job_name: str) -> str:
    for job in workflow["jobs"].values():
        if job["name"] != job_name:
            continue
        detect = [step for step in job["steps"] if step.get("id") == "shop_changes"]
        assert len(detect) == 1, job_name
        script = detect[0]["run"]
        assert isinstance(script, str)
        return script
    raise AssertionError(job_name)


def _detect_shop(script: str, paths: tuple[str, ...]) -> str:
    """Run one job's detect step as a pull request with a fixed changed list."""
    assignment = f'changed="$({DIFF_COMMAND})"'
    assert assignment in script
    if paths:
        quoted = " ".join("'" + path.replace("'", "'\\''") + "'" for path in paths)
        replacement = f"changed=$(printf '%s\\n' {quoted})"
    else:
        replacement = 'changed=""'
    patched = script.replace(assignment, replacement, 1)
    base = subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        text=True,
    ).strip()
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as handle:
        output_path = handle.name
    try:
        env = os.environ.copy()
        env["GITHUB_EVENT_NAME"] = "pull_request"
        env["SHOP_BASE_SHA"] = base
        env["GITHUB_OUTPUT"] = output_path
        completed = subprocess.run(
            ["bash", "-c", patched],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        assert completed.returncode == 0, completed.stderr
        written = Path(output_path).read_text(encoding="utf-8")
    finally:
        Path(output_path).unlink(missing_ok=True)
    flags = re.findall(r"(?m)^shop=(true|false)$", written)
    assert flags, written
    return flags[-1]


def _assert_readme_only_change_sets_shop_true(workflow: dict) -> None:
    """Pytest reads shop-app markdown and shop-web sources, so those diffs set shop=true.

    A README under api/ or web/ sets shop=true for shop-api pytest only.
    A shop-web .tsx, .html, .ts, or package.json change does too. Other docs,
    and the lint and visual jobs for markdown, still leave shop=false.
    """
    shop_api = _detect_script(workflow, "shop-api pytest")
    shop_web = _detect_script(workflow, "shop-web lint / typecheck / build")
    visual = _detect_script(workflow, VISUAL_CHECK_NAME)
    readme_only = (
        "apps/project-car/api/README.md",
        "apps/project-car/web/README.md",
        "apps/project-car/api/docs/guide.md",
        "apps/project-car/web/lib/notes.md",
    )
    for path in readme_only:
        assert _detect_shop(shop_api, (path,)) == "true", path
        assert _detect_shop(shop_web, (path,)) == "false", path
        assert _detect_shop(visual, (path,)) == "false", path

    other_docs = (
        "Docs/shop-os-ci.md",
        "README.md",
        "apps/project-car/ci-path-probe.md",
        "apps/website/README.md",
        "apps/project-car/api/notes.txt",
    )
    for path in other_docs:
        assert _detect_shop(shop_api, (path,)) == "false", path
        assert _detect_shop(shop_web, (path,)) == "false", path
        assert _detect_shop(visual, (path,)) == "false", path

    assert _detect_shop(shop_api, ("apps/project-car/api/app/main.py",)) == "true"
    assert _detect_shop(shop_web, ("apps/project-car/web/app/page.tsx",)) == "true"
    # Pytest reads these shop-web paths, so a page.tsx-only diff must set shop=true.
    shop_web_sources = (
        "apps/project-car/web/app/page.tsx",
        "apps/project-car/web/components/owner-demo-banner.tsx",
        "apps/project-car/web/public/offline.html",
        "apps/project-car/web/lib/placeholders.ts",
        "apps/project-car/web/package.json",
        "apps/project-car/web/visual/pages.spec.ts",
        "apps/project-car/web/playwright.config.ts",
    )
    for path in shop_web_sources:
        assert _detect_shop(shop_api, (path,)) == "true", path


def test_shop_os_ci_path_filter_keeps_required_check_names() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    workflow = parse_workflow_yaml(text)

    assert workflow["permissions"] == {"contents": "read"}
    assert "${{ secrets" not in text
    assert re.search(r"(?m)^\s*secrets\s*:", text) is None

    jobs = workflow["jobs"]
    names = [job["name"] for job in jobs.values()]
    assert names == [*REQUIRED_CHECK_NAMES, VISUAL_CHECK_NAME]

    # 0.1 layout shift and 1% pixel ratio (maxDiffPixelRatio 0.01).
    pages = PAGES.read_text(encoding="utf-8")
    playwright = PLAYWRIGHT.read_text(encoding="utf-8")
    runbook = RUNBOOK.read_text(encoding="utf-8")
    package = PACKAGE.read_text(encoding="utf-8")
    assert "const MAX_LAYOUT_SHIFT = 0.1;" in pages
    assert "maxDiffPixelRatio: 0.01," in playwright
    assert "layout shift goes above 0.1" in runbook
    assert "more than 1% of pixels" in runbook
    assert '"typecheck": "tsc --noEmit"' in package

    trigger = workflow["on"]
    pull_request = trigger["pull_request"]
    push = trigger["push"]
    assert pull_request is None or "paths" not in pull_request
    assert "paths" not in push
    assert not _contains_key(trigger, "paths")
    assert push["branches"] == ["main"]

    for job in jobs.values():
        assert "if" not in job, job["name"]
        steps = job["steps"]
        detect = [step for step in steps if step.get("id") == "shop_changes"]
        assert detect, (
            f"{job['name']} has no changes gate, so a docs-only pull request "
            "cannot keep this check green without running the heavy steps"
        )
        assert len(detect) == 1
        assert steps[0]["name"] == "Checkout"
        assert steps[0]["uses"] == "actions/checkout@v4"
        assert steps[0].get("with", {}).get("fetch-depth") == 0
        assert "if" not in steps[0]
        assert steps[1]["name"] == "Detect Shop OS changes"
        assert steps[1] is detect[0]
        assert "if" not in steps[1]
        script = steps[1]["run"]
        assert isinstance(script, str)
        assert DIFF_COMMAND in script
        assert "apps/project-car/" in script
        assert ".github/workflows/shop-os-ci.yml" in script
        assert PUSH_GUARD in script
        assert script.index(PUSH_GUARD) < script.index(DIFF_COMMAND)
        assert "shop=true" in script[: script.index(DIFF_COMMAND)]
        for step in steps[2:]:
            step_if = step.get("if")
            name = step.get("name")
            if name not in {"Prepare screenshot baselines", "Store screenshot baselines"}:
                assert step_if == GATE_IF, name
            if name == "Prepare screenshot baselines":
                assert step_if == BASELINE_PREPARE_IF
            if name == "Store screenshot baselines":
                assert step_if == BASELINE_STORE_IF
                assert step.get("uses") == "actions/cache/save@v4"
        if job["name"] == VISUAL_CHECK_NAME:
            restore = [step for step in steps if step.get("name") == "Restore screenshot baselines"]
            store = [step for step in steps if step.get("name") == "Store screenshot baselines"]
            assert len(restore) == 1 and len(store) == 1
            assert restore[0].get("id") == "screenshot_baselines"
            assert restore[0]["if"] == GATE_IF
            baseline_key = "shop-web-screenshot-baselines-${{ github.sha }}"
            assert restore[0]["with"]["key"] == baseline_key
            assert store[0]["with"]["key"] == baseline_key
        for command in HEAVY_COMMANDS[job["name"]]:
            matched = [step for step in steps if step.get("run") == command]
            assert len(matched) == 1, command
            assert matched[0]["if"] == GATE_IF

    _assert_readme_only_change_sets_shop_true(workflow)


def _job_script(job_name: str) -> str:
    workflow = parse_workflow_yaml(WORKFLOW.read_text(encoding="utf-8"))
    for job in workflow["jobs"].values():
        if job["name"] == job_name:
            script = job["steps"][1]["run"]
            assert isinstance(script, str)
            return script
    raise AssertionError(job_name)


def _shop_flags(script: str, paths: list[str]) -> dict[str, str]:
    """Run the detect loop the way the job does, one changed path at a time."""
    start = script.index("shop=false\n")
    end = script.index('echo "shop=${shop}"')
    loop = script[start:end]
    program = f"""
set -eu
shop_for() {{
  changed="$1"
{loop}
  printf '%s\\n' "$shop"
}}
while IFS= read -r line; do
  [ -n "$line" ] || continue
  shop_for "$line"
done
"""
    result = subprocess.run(
        ["bash", "-c", program],
        input="".join(f"{path}\n" for path in paths),
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    flags = result.stdout.splitlines()
    assert len(flags) == len(paths), result.stdout
    return dict(zip(paths, flags, strict=True))


def test_shop_api_runs_for_booking_cancel_and_owner_booking_card() -> None:
    """API tests read these web files, so a pull request that touches them runs pytest."""
    script = _job_script("shop-api pytest")
    web_root = ROOT / "apps" / "project-car" / "web"
    paths = [
        "apps/project-car/web/lib/booking-cancel.test.ts",
        "apps/project-car/web/components/owner-booking-card.tsx",
        "apps/project-car/web/components/member-booking-card.tsx",
        "apps/project-car/web/visual/pages.spec.ts",
        "apps/project-car/web/visual/active-visit-cancel.spec.ts",
        "apps/project-car/web/playwright.config.ts",
        "apps/project-car/web/package.json",
    ]
    paths.extend(
        path.relative_to(ROOT).as_posix()
        for path in web_root.rglob("*")
        if path.is_file() and path.suffix.lower() in {".tsx", ".html"}
    )
    flags = _shop_flags(script, paths)
    assert flags["apps/project-car/web/lib/booking-cancel.test.ts"] == "true"
    assert flags["apps/project-car/web/components/owner-booking-card.tsx"] == "true"
    missed = [path for path, flag in flags.items() if flag != "true"]
    assert missed == []
    readmes = _shop_flags(
        script,
        [
            "apps/project-car/web/README.md",
            "apps/project-car/api/README.md",
            "apps/project-car/web/copy/hours.md",
            "apps/project-car/web/visual/screenshots/390/home.png",
            "Docs/shop-os-ci.md",
            "README.md",
        ],
    )
    assert readmes["apps/project-car/web/README.md"] == "true"
    assert readmes["apps/project-car/api/README.md"] == "true"
    assert readmes["apps/project-car/web/copy/hours.md"] == "true"
    assert readmes["apps/project-car/web/visual/screenshots/390/home.png"] == "false"
    assert readmes["Docs/shop-os-ci.md"] == "false"
    assert readmes["README.md"] == "false"


def test_api_only_runs_screenshots_skips_web_build_and_reuses_baselines() -> None:
    """API-only diffs skip the web build and still render screenshots. Baselines come from main."""
    api_path = "apps/project-car/api/app/__init__.py"
    web_paths = (
        "apps/project-car/web/lib/booking-cancel.test.ts",
        "apps/project-car/web/components/owner-booking-card.tsx",
    )
    shared_path = "apps/project-car/shared/contract.json"
    workflow_path = ".github/workflows/shop-os-ci.yml"
    doc_path = "apps/project-car/web/README.md"
    jobs = (
        "shop-api pytest",
        "shop-web lint / typecheck / build",
        "shop-web layout-shift / screenshots",
    )
    flags = {
        name: _shop_flags(_job_script(name), [api_path, *web_paths, shared_path, workflow_path, doc_path])
        for name in jobs
    }
    assert flags["shop-api pytest"][api_path] == "true"
    assert flags["shop-web lint / typecheck / build"][api_path] == "false"
    assert flags["shop-web layout-shift / screenshots"][api_path] == "true"
    for path in web_paths:
        assert flags["shop-api pytest"][path] == "true", path
        assert flags["shop-web lint / typecheck / build"][path] == "true", path
        assert flags["shop-web layout-shift / screenshots"][path] == "true", path
    for path in (shared_path, workflow_path):
        for name in jobs:
            assert flags[name][path] == "true", (name, path)
    assert flags["shop-api pytest"][doc_path] == "true"
    assert flags["shop-web lint / typecheck / build"][doc_path] == "false"
    assert flags["shop-web layout-shift / screenshots"][doc_path] == "false"

    text = WORKFLOW.read_text(encoding="utf-8")
    assert "cache: pip" in text
    assert "cache: npm" in text
    assert "shop-api-venv-" in text
    assert "shop-web-modules-" in text
    modules_key = (
        "shop-web-modules-${{ runner.os }}-${{ hashFiles("
        "'apps/project-car/web/package-lock.json', "
        "'apps/project-car/web/package.json') }}"
    )
    assert text.count(modules_key) == 2
    assert "shop-web-screenshot-baselines-" in text
    assert "bash visual/apply-baselines.sh" in text
    assert "actions/cache/restore@v4" in text
    assert "actions/cache/save@v4" in text
    apply = ROOT / "apps" / "project-car" / "web" / "visual" / "apply-baselines.sh"
    script = apply.read_text(encoding="utf-8")
    assert "git checkout" not in script
    assert "npm run build" not in script
    assert "no stored screenshot baseline" in script

    with tempfile.TemporaryDirectory() as temporary:
        visual = Path(temporary)
        shots = visual / "screenshots" / "390"
        shots.mkdir(parents=True)
        committed = shots / "home.png"
        committed.write_bytes(b"committed")
        probe_env = os.environ.copy()
        probe_env["VISUAL_DIR"] = str(visual)
        probe_env["GITHUB_EVENT_NAME"] = "pull_request"
        probe_env.pop("SHOP_BASE_SHA", None)
        missing = subprocess.run(
            ["sh", str(apply)],
            check=False,
            capture_output=True,
            text=True,
            env=probe_env,
        )
        assert missing.returncode == 0, missing.stderr
        assert "no stored screenshot baseline" in missing.stdout
        assert committed.read_bytes() == b"committed"
        baseline = visual / "screenshot-baselines" / "390"
        baseline.mkdir(parents=True)
        (baseline / "home.png").write_bytes(b"from-main")
        applied = subprocess.run(
            ["sh", str(apply)],
            check=False,
            capture_output=True,
            text=True,
            env=probe_env,
        )
        assert applied.returncode == 0, applied.stderr
        assert "stored screenshot baselines" in applied.stdout
        assert committed.read_bytes() == b"from-main"

        committed.write_bytes(b"checkout-on-push")
        (baseline / "home.png").write_bytes(b"baseline-on-push")
        push_env = probe_env.copy()
        push_env["GITHUB_EVENT_NAME"] = "push"
        push_env.pop("SHOP_BASE_SHA", None)
        pushed = subprocess.run(
            ["sh", str(apply)],
            check=False,
            capture_output=True,
            text=True,
            env=push_env,
        )
        assert pushed.returncode == 0, pushed.stderr
        assert "push compares against the screenshots in this checkout" in pushed.stdout
        assert committed.read_bytes() == b"checkout-on-push"
        assert (baseline / "home.png").read_bytes() == b"baseline-on-push"

    screenshot = "apps/project-car/web/visual/screenshots/390/home.png"
    with tempfile.TemporaryDirectory() as repo_dir:
        repo = Path(repo_dir)
        checkout = repo / screenshot
        checkout.parent.mkdir(parents=True)
        checkout.write_bytes(b"base-png")
        git_env = os.environ.copy()
        git_base = [
            "git",
            "-C",
            str(repo),
            "-c",
            "user.name=Project Car",
            "-c",
            "user.email=project-car@example.com",
            "-c",
            "commit.gpgsign=false",
        ]

        def git(*args: str) -> subprocess.CompletedProcess[str]:
            return subprocess.run(
                [*git_base, *args],
                check=False,
                capture_output=True,
                text=True,
                env=git_env,
            )

        init = git("init")
        assert init.returncode == 0, init.stderr
        assert git("add", screenshot).returncode == 0
        base_commit = git("commit", "-m", "base screenshot")
        assert base_commit.returncode == 0, base_commit.stderr
        base_sha = git("rev-parse", "HEAD")
        assert base_sha.returncode == 0, base_sha.stderr
        checkout.write_bytes(b"pr-png")
        assert git("add", screenshot).returncode == 0
        pr_commit = git("commit", "-m", "edit screenshot")
        assert pr_commit.returncode == 0, pr_commit.stderr
        changed = git("diff", "--name-only", "--no-renames", base_sha.stdout.strip(), "HEAD")
        assert changed.returncode in {0, 1}, changed.stderr
        assert screenshot in changed.stdout
        visual_dir = repo / "apps" / "project-car" / "web" / "visual"
        stored = visual_dir / "screenshot-baselines" / "390" / "home.png"
        stored.parent.mkdir(parents=True)
        stored.write_bytes(b"stored-baseline")
        pr_env = os.environ.copy()
        pr_env["VISUAL_DIR"] = str(visual_dir)
        pr_env["GITHUB_EVENT_NAME"] = "pull_request"
        pr_env["SHOP_BASE_SHA"] = base_sha.stdout.strip()
        edited = subprocess.run(
            ["sh", str(apply)],
            check=False,
            capture_output=True,
            text=True,
            env=pr_env,
        )
        assert edited.returncode == 0, edited.stderr
        assert "pull request edits screenshot baselines" in edited.stdout
        assert checkout.read_bytes() == b"pr-png"
        assert stored.read_bytes() == b"stored-baseline"


def _detect_on_push(script: str) -> str:
    """A push must set shop=true before the pull-request base sha is checked."""
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as handle:
        output_path = handle.name
    try:
        env = os.environ.copy()
        env["GITHUB_EVENT_NAME"] = "push"
        env["GITHUB_OUTPUT"] = output_path
        env["SHOP_BASE_SHA"] = "not-a-sha"
        completed = subprocess.run(
            ["bash", "-c", script],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        assert completed.returncode == 0, completed.stderr
        written = Path(output_path).read_text(encoding="utf-8")
    finally:
        Path(output_path).unlink(missing_ok=True)
    flags = re.findall(r"(?m)^shop=(true|false)$", written)
    assert flags, written
    return flags[-1]


def test_visual_markdown_and_other_images_skip_heavy_steps() -> None:
    """Screenshot PNGs are the image exception. Other images, and markdown, are not.

    `apps/project-car/web/visual/README.md` is markdown under shop-web, so shop-api
    pytest still runs and the visual job does not. `.webp` and `.SVG` are images,
    so none of the three jobs run their heavy steps for them. `shop-now.txt` still
    runs the visual job because the screenshot build bakes that clock in.
    """
    text = WORKFLOW.read_text(encoding="utf-8")
    workflow = parse_workflow_yaml(text)
    jobs = workflow["jobs"]
    assert jobs["shop-api"]["timeout-minutes"] == 10
    assert jobs["shop-web"]["timeout-minutes"] == 10
    assert workflow["concurrency"]["cancel-in-progress"] == (
        "${{ github.event_name == 'pull_request' }}"
    )
    visual_job = jobs["shop-web-visual"]
    cache = [step for step in visual_job["steps"] if step.get("id") == "pw_cache"]
    assert len(cache) == 1
    assert cache[0]["uses"] == "actions/cache@v4"
    assert cache[0]["with"]["path"] == "~/.cache/ms-playwright"
    install = [step for step in visual_job["steps"] if step.get("name") == "Install Playwright Chromium"]
    assert len(install) == 1
    assert "npx playwright install-deps chromium" in install[0]["run"]
    assert "npx playwright install --with-deps chromium" in install[0]["run"]

    shop_api = _detect_script(workflow, "shop-api pytest")
    shop_web = _detect_script(workflow, "shop-web lint / typecheck / build")
    visual = _detect_script(workflow, VISUAL_CHECK_NAME)
    for script in (shop_api, shop_web, visual):
        assert _detect_on_push(script) == "true"

    readme = "apps/project-car/web/visual/README.md"
    assert _detect_shop(shop_api, (readme,)) == "true"
    assert _detect_shop(shop_web, (readme,)) == "false"
    assert _detect_shop(visual, (readme,)) == "false"

    png = "apps/project-car/web/visual/screenshots/390/home.png"
    assert _detect_shop(visual, (png,)) == "true"
    assert _detect_shop(shop_api, (png,)) == "false"
    assert _detect_shop(shop_web, (png,)) == "false"

    clock = "apps/project-car/web/visual/shop-now.txt"
    assert _detect_shop(visual, (clock,)) == "true"
    assert _detect_shop(shop_api, (clock,)) == "false"
    assert _detect_shop(shop_web, (clock,)) == "false"

    spec = "apps/project-car/web/visual/pages.spec.ts"
    assert _detect_shop(shop_api, (spec,)) == "true"
    assert _detect_shop(shop_web, (spec,)) == "true"
    assert _detect_shop(visual, (spec,)) == "true"

    images = (
        "apps/project-car/api/icon.SVG",
        "apps/project-car/web/public/mark.SVG",
        "apps/project-car/web/visual/mark.SVG",
        "apps/project-car/web/logo.webp",
        "apps/project-car/web/visual/logo.webp",
        "apps/project-car/logo.webp",
    )
    for path in images:
        assert _detect_shop(shop_api, (path,)) == "false", path
        assert _detect_shop(shop_web, (path,)) == "false", path
        assert _detect_shop(visual, (path,)) == "false", path
