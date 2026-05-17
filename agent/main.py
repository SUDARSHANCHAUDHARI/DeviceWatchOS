"""DeviceWatch OS agent CLI."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from platform import node, platform

from agent.collectors.cpu import collect_cpu
from agent.collectors.memory import collect_memory
from agent.collectors.network import collect_network
from agent.collectors.processes import collect_processes
from agent.collectors.usb import collect_usb

SUSPICIOUS_PROCESS_TERMS = ("miner", "xmrig", "nc ", "netcat", "reverse", "tunnel", "bash -c")


def collect_snapshot() -> dict:
    """Collect a local device telemetry snapshot."""
    return {
        "device_id": node() or "unknown-device",
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "platform": platform(),
        "heartbeat": {"status": "online"},
        "cpu": collect_cpu(),
        "memory": collect_memory(),
        "network": collect_network(),
        "usb": collect_usb(),
        "processes": collect_processes(),
    }


def analyze_snapshot(snapshot: dict) -> list[dict]:
    """Analyze telemetry and return alerts."""
    alerts: list[dict] = []
    memory = snapshot.get("memory", {})
    if float(memory.get("used_percent", 0)) >= 90:
        alerts.append(
            {
                "kind": "health.memory_high",
                "severity": "high",
                "summary": "Memory usage is above the configured threshold.",
                "evidence": memory,
            }
        )

    cpu = snapshot.get("cpu", {})
    cpu_count = max(int(cpu.get("cpu_count", 1)), 1)
    if float(cpu.get("load_1m", 0)) > cpu_count * 2:
        alerts.append(
            {
                "kind": "health.cpu_load_high",
                "severity": "medium",
                "summary": "One-minute CPU load is unusually high for this device.",
                "evidence": cpu,
            }
        )

    for process in snapshot.get("processes", []):
        args = str(process.get("args", "")).lower()
        if any(term in args for term in SUSPICIOUS_PROCESS_TERMS):
            alerts.append(
                {
                    "kind": "security.suspicious_process",
                    "severity": "high",
                    "summary": "Process command line matches a suspicious pattern.",
                    "evidence": process,
                }
            )

    if snapshot.get("usb"):
        alerts.append(
            {
                "kind": "security.usb_present",
                "severity": "low",
                "summary": "USB devices are present and should be checked against the expected baseline.",
                "evidence": {"usb_count": len(snapshot["usb"])},
            }
        )
    return alerts


def build_report(snapshot: dict, alerts: list[dict]) -> str:
    """Return a Markdown device health and security report."""
    lines = [
        "# DeviceWatch OS Report",
        "",
        f"- Device: `{snapshot.get('device_id')}`",
        f"- Captured: {snapshot.get('captured_at')}",
        f"- Alerts: {len(alerts)}",
        "",
        "## Telemetry",
        "",
        f"- CPU: `{snapshot.get('cpu')}`",
        f"- Memory: `{snapshot.get('memory')}`",
        f"- Network: `{snapshot.get('network')}`",
        f"- USB devices: {len(snapshot.get('usb', []))}",
        "",
        "## Alerts",
        "",
    ]
    if not alerts:
        lines.append("No alerts generated.")
    for alert in alerts:
        lines.extend(
            [
                f"### {alert['summary']}",
                "",
                f"- Severity: `{alert['severity']}`",
                f"- Type: `{alert['kind']}`",
                f"- Evidence: `{alert['evidence']}`",
                "",
            ]
        )
    return "\n".join(lines) + "\n"


def load_snapshot(path: Path) -> dict:
    """Load a telemetry snapshot."""
    return json.loads(path.read_text(encoding="utf-8"))


def write_outputs(snapshot: dict, alerts: list[dict], out_dir: Path) -> None:
    """Write MVP artifacts."""
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "snapshot.json").write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out_dir / "alerts.json").write_text(json.dumps(alerts, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out_dir / "report.md").write_text(build_report(snapshot, alerts), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="DeviceWatch OS agent MVP")
    parser.add_argument("--sample", type=Path, help="Analyze an existing snapshot instead of collecting locally")
    parser.add_argument("--out-dir", type=Path, default=Path("data/reports"))
    args = parser.parse_args()

    snapshot = load_snapshot(args.sample) if args.sample else collect_snapshot()
    alerts = analyze_snapshot(snapshot)
    write_outputs(snapshot, alerts, args.out_dir)
    print(f"Device: {snapshot.get('device_id')}")
    print(f"Generated {len(alerts)} alert(s)")


if __name__ == "__main__":
    main()
