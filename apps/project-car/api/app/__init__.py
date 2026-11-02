"""Project Car shop OS API."""

from __future__ import annotations

import os
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo, reset_tzpath

import tzdata

__version__ = "0.1.0"

# Alberta is permanent UTC-6 from 2026-11-01 (IANA 2026c, packaged as tzdata>=2026.3).
_EDMONTON_UTC_MINUS_6 = (
    datetime(2026, 11, 1, 3, 0),
    datetime(2026, 12, 15, 12, 0),
)


def _prefer_packaged_tzdata() -> None:
    """Read zoneinfo from the tzdata package, not the host database.

    On Linux, zoneinfo uses the system tzdata whenever TZPATH is set, and
    never the installed package. A host older than 2026c puts
    America/Edmonton on UTC-7 at 2026-11-01 02:00.
    """
    zoneinfo_dir = Path(tzdata.__file__).resolve().parent / "zoneinfo"
    if not zoneinfo_dir.is_dir():
        raise RuntimeError(f"tzdata zoneinfo is missing: {zoneinfo_dir}")
    os.environ["PYTHONTZPATH"] = str(zoneinfo_dir)
    reset_tzpath(to=[str(zoneinfo_dir)])
    ZoneInfo.clear_cache()

    edmonton = ZoneInfo("America/Edmonton")
    for stamp in _EDMONTON_UTC_MINUS_6:
        offset = stamp.replace(tzinfo=edmonton).utcoffset()
        if offset != timedelta(hours=-6):
            if offset is None:
                hours = "missing"
            else:
                hours = f"{offset.total_seconds() / 3600:+.0f}h"
            raise RuntimeError(
                "Refusing to start: America/Edmonton is "
                f"{hours} at {stamp.isoformat()}, not -6h. "
                "Install tzdata>=2026.3 (IANA 2026c)."
            )


_prefer_packaged_tzdata()
