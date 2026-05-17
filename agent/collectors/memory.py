"""Memory collector."""

from __future__ import annotations

from pathlib import Path


def collect_memory() -> dict:
    """Return memory usage telemetry from /proc when available."""
    meminfo = Path("/proc/meminfo")
    if not meminfo.exists():
        return {"total_kb": 0, "available_kb": 0, "used_percent": 0.0}

    values: dict[str, int] = {}
    for line in meminfo.read_text(encoding="utf-8", errors="replace").splitlines():
        key, _, rest = line.partition(":")
        amount = rest.strip().split()[0] if rest.strip() else "0"
        if amount.isdigit():
            values[key] = int(amount)
    total = values.get("MemTotal", 0)
    available = values.get("MemAvailable", 0)
    used_percent = 0.0 if not total else round(((total - available) / total) * 100, 2)
    return {"total_kb": total, "available_kb": available, "used_percent": used_percent}
