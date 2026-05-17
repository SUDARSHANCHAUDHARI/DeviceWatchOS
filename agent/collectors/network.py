"""Network collector."""

from __future__ import annotations

from pathlib import Path


def collect_network() -> dict:
    """Return network interface counters from /proc when available."""
    net_dev = Path("/proc/net/dev")
    interfaces: list[dict] = []
    if net_dev.exists():
        for line in net_dev.read_text(encoding="utf-8", errors="replace").splitlines()[2:]:
            name, _, counters = line.partition(":")
            parts = counters.split()
            if len(parts) >= 16:
                interfaces.append(
                    {
                        "name": name.strip(),
                        "rx_bytes": int(parts[0]),
                        "tx_bytes": int(parts[8]),
                    }
                )
    return {"interfaces": interfaces, "interface_count": len(interfaces)}
