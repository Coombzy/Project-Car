import pathlib
import re
import subprocess
import sys

root = pathlib.Path(__file__).resolve().parents[1]
restore_path = root / "scripts" / "restore-drill.sh"
pytest_path = root / "apps/project-car/api/tests/test_backup_restore.py"


def fail(msg):
    print(msg, file=sys.stderr)
    raise SystemExit(1)


restore = restore_path.read_text(encoding="utf-8")
text = pytest_path.read_text(encoding="utf-8")
refuse_at = restore.find("exit 2")
client_at = len(restore)
for token in ("psql", "dropdb", "pg_dump", "pg_restore", "createdb"):
    idx = restore.find(token)
    if idx != -1 and idx < client_at:
        client_at = idx
if refuse_at < 0 or refuse_at > client_at:
    fail("same-name refusal is not before any client connection")
for needle in (
    "RESTORE_DRILL_TAMPER_SQL",
    "alembic current",
    "members",
    "bookings",
    "token_transactions",
    "billing_transactions",
    "reconcile_ledger.py",
):
    if needle not in restore:
        fail("missing " + needle)
drops = re.findall(r"DROP\s+DATABASE(?:\s+IF\s+EXISTS)?\s+(\S+)", restore, re.I)
if not drops or any(item.strip("\"'`") != "projectcar_restore_check" for item in drops):
    fail("drop is not the literal throwaway name")
if not re.search(r"skipif\([^)]*DATABASE_URL", text):
    fail("pytest does not skip without DATABASE_URL")
for needle in ("equal counts", "exit 0", "tamper", "exit 1", "same-name", "exit 2", "untouched"):
    if needle not in text:
        fail("pytest missing " + needle)
guard = subprocess.run(
    [sys.executable, "scripts/test_backup_script_guards.py"],
    cwd=root,
    capture_output=True,
    text=True,
    timeout=30,
)
if guard.returncode != 0 or "ok" not in guard.stdout:
    fail(guard.stdout + guard.stderr)
live = subprocess.run(
    [str(restore_path)],
    cwd=root,
    env={"PATH": "/usr/bin:/bin", "DATABASE_URL": "postgresql:///projectcar_restore_check"},
    capture_output=True,
    text=True,
    timeout=10,
)
blob = live.stdout + live.stderr
if live.returncode != 2 or "would be dropped" not in blob:
    fail(blob)
print("ok")
