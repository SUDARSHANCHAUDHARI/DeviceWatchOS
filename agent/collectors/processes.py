"""Process collector."""

from __future__ import annotations

import subprocess


def collect_processes() -> list[dict]:
    """Return process telemetry."""
    try:
        result = subprocess.run(
            ["ps", "-axo", "pid=,user=,comm=,args="],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return []

    processes: list[dict] = []
    for line in result.stdout.splitlines():
        parts = line.strip().split(None, 3)
        if len(parts) < 4:
            continue
        pid, user, command, args = parts
        processes.append({"pid": pid, "user": user, "command": command, "args": args})
    return processes
