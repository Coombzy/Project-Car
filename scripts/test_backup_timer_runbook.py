"""No-daemon check for the backup timer stub and restore runbook."""

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SERVICE = ROOT / "infra" / "systemd" / "project-car-backup.service"
TIMER = ROOT / "infra" / "systemd" / "project-car-backup.timer"
RUNBOOK = ROOT / "Docs" / "runbooks" / "backup-restore.md"

NEEDLES = (
    "DATABASE_URL",
    "BACKUP_REMOTE is unset",
    "stand-in-remote:project-car-backups",
    "monthly",
    "projectcar_restore_check",
    "never dropped",
)


def main() -> int:
    missing = [str(path.relative_to(ROOT)) for path in (SERVICE, TIMER, RUNBOOK) if not path.is_file()]
    if missing:
        print("missing " + ", ".join(missing), file=sys.stderr)
        return 1

    problems = []
    timer = TIMER.read_text(encoding="utf-8")
    service = SERVICE.read_text(encoding="utf-8")
    runbook = RUNBOOK.read_text(encoding="utf-8")
    if "OnCalendar=*-*-* 03:15:00 America/Regina" not in timer:
        problems.append("timer OnCalendar")
    if "Type=oneshot" not in service or "backup-db.sh" not in service:
        problems.append("service oneshot/backup-db.sh")
    for needle in NEEDLES:
        if needle not in runbook:
            problems.append("runbook " + needle)
    if problems:
        print("fail: " + "; ".join(problems), file=sys.stderr)
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
