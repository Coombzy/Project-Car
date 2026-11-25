# Shop database backup and restore drill

Scripts on this tree: `scripts/backup-db.sh` and `scripts/restore-drill.sh`. Both read the DSN only from `DATABASE_URL`. Neither file embeds a password, host, or remote name.

Install `scripts/backup-db.sh` as `/usr/local/sbin/backup-db.sh` (the path in `infra/systemd/project-car-backup.service`). Put `DATABASE_URL` in a systemd drop-in. Do not put it in the unit file. Do not enable or start the unit from this repo.

## Backup

`backup-db.sh` exits 1 when `DATABASE_URL` is empty. Otherwise it runs `pg_dump -Fc` into `BACKUP_DIR` (default `/var/backups/project-car`) as `projectcar-<UTC stamp>.dump`.

Off-site copy runs only when `BACKUP_REMOTE` is set (`rclone copy` of that dump). When `BACKUP_REMOTE` is unset the script prints `skip off-site rclone copy: BACKUP_REMOTE is unset` and exits 0. There is no default remote name.

Stand-in remote for docs, until Ben picks B2 or R2: `stand-in-remote:project-car-backups`.

`infra/systemd/project-car-backup.timer` is a stub. It schedules `project-car-backup.service` (`Type=oneshot`, `ExecStart` runs `backup-db.sh`) with `OnCalendar=*-*-* 03:15:00 America/Regina` so 03:15 is Regina time on a UTC host. `Persistent=true`. `WantedBy=timers.target`. Installing the files does not enable the timer.

## Restore drill

Operators should run the restore drill monthly with `scripts/restore-drill.sh`.

The drill dumps `DATABASE_URL` to a temp file, then restores into the throwaway database `projectcar_restore_check` only. It drops and creates that literal name. The source database is never dropped.

Before any client connection, the script exits 2 with `refusing: source database would be dropped` when the source name is `projectcar_restore_check`, when `RESTORE_TARGET_DB` is set to the source name, or when the throwaway URL would still name the source. Same-name refusal is what keeps the source from being dropped.
