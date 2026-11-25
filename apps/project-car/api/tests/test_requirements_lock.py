"""AUD-059: requirements.lock exists and pins direct dependencies from pyproject.toml.

The lock is the constraints file compiled from pyproject.toml. It must name
every direct project dependency and the dev extra. CI cache keys stay on
pyproject.toml; this test only checks the lock file.
"""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

API_ROOT = Path(__file__).resolve().parents[1]
LOCK = API_ROOT / "requirements.lock"
_SPEC_NAME = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*)")


def _pep503(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def _spec_name(spec: str) -> str:
    match = _SPEC_NAME.match(spec.strip())
    if match is None:
        raise AssertionError(f"unparsed dependency: {spec}")
    return _pep503(match.group(1))


def _direct_names() -> list[str]:
    project = tomllib.loads((API_ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    specs = list(project["dependencies"])
    specs.extend(project["optional-dependencies"]["dev"])
    return [_spec_name(spec) for spec in specs]


def _locked_names(text: str) -> set[str]:
    names: set[str] = set()
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        pinned = line.split(";", 1)[0].strip()
        if "==" not in pinned:
            continue
        names.add(_pep503(pinned.split("==", 1)[0].split("[", 1)[0].strip()))
    return names


def test_requirements_lock_exists_and_lists_direct_dependencies() -> None:
    assert LOCK.is_file(), "requirements.lock is missing"
    missing = [name for name in _direct_names() if name not in _locked_names(LOCK.read_text(encoding="utf-8"))]
    assert missing == [], "requirements.lock missing direct dependencies: " + ", ".join(missing)
