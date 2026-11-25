import pathlib
import re
import subprocess
import sys

root = pathlib.Path(__file__).resolve().parents[1]
backup = root / "scripts" / "backup-db.sh"
restore = root / "scripts" / "restore-drill.sh"
BAKED = re.compile(
    r"://[^\s/:@]+:[^@\s]+@|\bPGPASSWORD\s*=\s*\S+|\bpassword\s*=\s*['\"][^'\"]+['\"]",
    re.I,
)


def fail(msg):
    print(msg, file=sys.stderr)
    raise SystemExit(1)


def load_script(path):
    if not path.is_file():
        fail("missing " + path.name)
    if path.stat().st_mode & 0o111 == 0:
        fail("not executable: " + path.name)
    text = path.read_text(encoding="utf-8")
    if "DATABASE_URL" not in text:
        fail(path.name + " does not mention DATABASE_URL")
    if BAKED.search(text):
        fail(path.name + " contains a baked password")
    return text


backup_text = load_script(backup)
restore_text = load_script(restore)

if "BACKUP_REMOTE" not in backup_text or "rclone" not in backup_text:
    fail("backup-db.sh missing off-site copy path")
if not re.search(r"-z\s+.\$\{BACKUP_REMOTE:-\}", backup_text):
    fail("backup-db.sh missing BACKUP_REMOTE unset skip path")
if "skip" not in backup_text.lower():
    fail("backup-db.sh missing BACKUP_REMOTE skip message")
if re.search(r"\$\{BACKUP_REMOTE:-[^}]+\}", backup_text):
    fail("backup-db.sh invents a default remote")

refuse_at = restore_text.find("exit 2")
client_at = len(restore_text)
for token in ("psql", "dropdb", "pg_dump", "pg_restore", "createdb"):
    idx = restore_text.find(token)
    if idx != -1:
        client_at = min(client_at, idx)
if refuse_at < 0 or refuse_at > client_at:
    fail("same-name refusal is not before any client connection")


def run_restore(env):
    proc = subprocess.run(
        [str(restore)],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        timeout=10,
    )
    out = proc.stdout + proc.stderr
    if proc.returncode != 2:
        fail("restore-drill exit %s, want 2: %s" % (proc.returncode, out))
    if "would not be dropped" not in out:
        fail("missing source refusal: " + out)
    if re.search(r"(?i)(drop database|pg_dump|pg_restore|successfully dropped)", out):
        fail("printed a successful drop of the source: " + out)


base = {"PATH": "/usr/bin:/bin"}
run_restore(dict(base, DATABASE_URL="postgresql:///projectcar_restore_check"))
run_restore(dict(base, DATABASE_URL="postgresql:///shop", RESTORE_TARGET_DB="shop"))
print("ok")
