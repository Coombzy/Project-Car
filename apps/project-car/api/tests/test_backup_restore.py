"""Restore drill: equal counts exit 0, tamper exit 1, same-name exit 2 source untouched. Skips without DATABASE_URL."""
import os
import subprocess
from pathlib import Path

import pytest

pytestmark = pytest.mark.skipif(
    not os.environ.get("DATABASE_URL"),
    reason="skipped without DATABASE_URL",
)
ROOT = Path(__file__).resolve().parents[4]
SCRIPT = ROOT / "scripts" / "restore-drill.sh"


def _run(extra):
    env = os.environ.copy()
    env.update(extra)
    return subprocess.run(
        [str(SCRIPT)], cwd=ROOT, env=env, capture_output=True, text=True, timeout=180
    )


def test_equal_counts_exit_0():
    proc = _run({})
    assert proc.returncode == 0, proc.stderr


def test_tamper_exit_1():
    proc = _run({"RESTORE_DRILL_TAMPER_SQL": "TRUNCATE members CASCADE;"})
    assert proc.returncode == 1, proc.stderr


def test_same_name_exit_2_source_untouched():
    proc = _run({"DATABASE_URL": "postgresql:///projectcar_restore_check"})
    blob = proc.stdout + proc.stderr
    assert proc.returncode == 2
    assert "would be dropped" in blob
    assert "pg_dump" not in blob.lower()
