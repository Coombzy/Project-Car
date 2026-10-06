from __future__ import annotations

import re
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
PUSH_GUARD = 'if [ "${GITHUB_EVENT_NAME}" = "push" ]; then'


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
        assert "git diff --name-only" in script
        assert "apps/project-car/" in script
        assert ".github/workflows/shop-os-ci.yml" in script
        assert PUSH_GUARD in script
        assert script.index(PUSH_GUARD) < script.index("git diff --name-only")
        assert "shop=true" in script[: script.index("git diff --name-only")]
        for step in steps[2:]:
            assert step.get("if") == GATE_IF, step.get("name")
        for command in HEAVY_COMMANDS[job["name"]]:
            matched = [step for step in steps if step.get("run") == command]
            assert len(matched) == 1, command
            assert matched[0]["if"] == GATE_IF
