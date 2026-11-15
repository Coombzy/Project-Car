"""R62 dashboard link. The 404 page calls dashboardHref in the web app.

Same cases as apps/project-car/web/lib/error-pages-path.test.ts:
test_backslash_parse_base_stays_on_the_owner_dashboard and
test_control_character_pathname_stays_on_the_owner_dashboard.
A raw backslash or a raw control is not window.location.pathname.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

WEB = Path(__file__).resolve().parents[2] / "web"
NODE = r"""
import { dashboardHref } from "./lib/error-pages.ts";
const cases = JSON.parse(process.env.CASES);
for (const [path, want] of cases) {
  const got = dashboardHref(path);
  if (got !== want) {
    console.log(JSON.stringify({ path, got, want }));
    process.exit(1);
  }
}
"""
BACKSLASH_CASES = [
    ("/\\shop.invalid\\member\\nope", "/"),
    ("/\\SHOP.INVALID\\member\\nope", "/"),
    ("/\\user@shop.invalid\\member\\nope", "/"),
    ("/\\shop.invalid:443\\member\\nope", "/"),
    ("/member/nope", "/member"),
    ("/member/../schedule", "/"),
    ("/no-such-page", "/"),
]
CONTROL_CASES = [
    ("/member\t/nope", "/"),
    ("/member\n/nope", "/"),
    ("/member\r/schedule", "/"),
    ("/\tmember/nope", "/"),
    ("/member/nope\x00", "/"),
    ("/member/nope\x7f", "/"),
    ("/member/nope", "/member"),
    ("/member/schedule", "/member"),
    ("/member/../schedule", "/"),
    ("/no-such-page", "/"),
    ("/%09/member/nope", "/"),
]


def _assert_cases(cases: list[tuple[str, str]]) -> None:
    node = shutil.which("node")
    if node is None:
        pytest.skip("node is not installed")
    probe = subprocess.run([node, "--experimental-strip-types", "-e", ""], capture_output=True, text=True)
    if probe.returncode != 0:
        pytest.skip("node cannot load the TypeScript helper")
    proc = subprocess.run(
        [node, "--experimental-strip-types", "--input-type=module", "-e", NODE],
        cwd=WEB,
        env={**os.environ, "CASES": json.dumps(cases)},
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_backslash_parse_base_stays_on_the_owner_dashboard() -> None:
    _assert_cases(BACKSLASH_CASES)


def test_control_character_pathname_stays_on_the_owner_dashboard() -> None:
    _assert_cases(CONTROL_CASES)
