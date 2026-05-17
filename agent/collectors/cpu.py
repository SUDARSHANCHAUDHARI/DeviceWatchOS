"""CPU collector."""

from __future__ import annotations

import os


def collect_cpu() -> dict:
    """Return basic CPU load telemetry."""
    load_1, load_5, load_15 = os.getloadavg() if hasattr(os, "getloadavg") else (0.0, 0.0, 0.0)
    return {
        "cpu_count": os.cpu_count() or 1,
        "load_1m": round(load_1, 2),
        "load_5m": round(load_5, 2),
        "load_15m": round(load_15, 2),
    }
