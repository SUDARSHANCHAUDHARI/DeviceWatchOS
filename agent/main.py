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
SUSPICIOUS_REMOTE_PORTS = {22, 4444, 5555, 6667, 8080, 9001}
SEVERITY_ORDER = {"critical": 4, "high": 3, "medium": 2, "low": 1}
NEXT_STEPS = {
    "health.memory_high": "Inspect memory-heavy processes and restart the kiosk workload only after preserving telemetry.",
    "health.cpu_load_high": "Check process list, recent deployments, and browser rendering loops before rebooting.",
    "health.reboot_recent": "Confirm the reboot matches a maintenance window or known power event.",
    "security.suspicious_process": "Quarantine the process, capture command-line evidence, and compare against the approved image.",
    "security.unusual_outbound": "Validate the destination IP and port against expected device egress rules.",
    "security.usb_present": "Compare attached USB devices against the baseline for this location.",
}


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
    heartbeat = snapshot.get("heartbeat", {})
    uptime_seconds = heartbeat.get("uptime_seconds")
    if uptime_seconds is not None and int(uptime_seconds) < 900:
        alerts.append(
            {
                "kind": "health.reboot_recent",
                "severity": "medium",
                "summary": "Device rebooted recently and should be checked against the expected maintenance window.",
                "evidence": {"uptime_seconds": uptime_seconds, "status": heartbeat.get("status", "unknown")},
            }
        )

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

    for connection in snapshot.get("network", {}).get("connections", []):
        remote_port = int(connection.get("remote_port", 0))
        state = str(connection.get("state", "")).upper()
        if state == "ESTABLISHED" and remote_port in SUSPICIOUS_REMOTE_PORTS:
            alerts.append(
                {
                    "kind": "security.unusual_outbound",
                    "severity": "high" if remote_port in {4444, 5555, 9001} else "medium",
                    "summary": "Established outbound connection uses a port that should be reviewed.",
                    "evidence": connection,
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


def severity_counts(alerts: list[dict]) -> dict[str, int]:
    """Return alert counts by severity."""
    return {
        severity: sum(1 for alert in alerts if alert.get("severity") == severity)
        for severity in ("critical", "high", "medium", "low")
    }


def risk_score(alerts: list[dict]) -> int:
    """Return a bounded device risk score."""
    score = sum(SEVERITY_ORDER.get(str(alert.get("severity", "low")), 1) * 12 for alert in alerts)
    return min(score, 100)


def sort_alerts(alerts: list[dict]) -> list[dict]:
    """Sort alerts by severity for analyst review."""
    return sorted(alerts, key=lambda alert: SEVERITY_ORDER.get(str(alert.get("severity", "")), 0), reverse=True)


def build_dashboard_summary(snapshot: dict, alerts: list[dict]) -> dict:
    """Return compact dashboard data for API/UI layers."""
    counts = severity_counts(alerts)
    sorted_alerts = sort_alerts(alerts)
    return {
        "device_id": snapshot.get("device_id"),
        "captured_at": snapshot.get("captured_at"),
        "heartbeat_status": snapshot.get("heartbeat", {}).get("status", "unknown"),
        "risk_score": risk_score(alerts),
        "alert_count": len(alerts),
        "severity_counts": counts,
        "top_alerts": sorted_alerts[:3],
        "telemetry": {
            "cpu": snapshot.get("cpu", {}),
            "memory": snapshot.get("memory", {}),
            "network_interface_count": snapshot.get("network", {}).get("interface_count", 0),
            "usb_count": len(snapshot.get("usb", [])),
            "process_count": len(snapshot.get("processes", [])),
        },
    }


def build_report(snapshot: dict, alerts: list[dict]) -> str:
    """Return a Markdown device health and security report."""
    sorted_alerts = sort_alerts(alerts)
    summary = build_dashboard_summary(snapshot, sorted_alerts)
    lines = [
        "# DeviceWatch OS Report",
        "",
        f"- Device: `{snapshot.get('device_id')}`",
        f"- Captured: {snapshot.get('captured_at')}",
        f"- Heartbeat: `{summary['heartbeat_status']}`",
        f"- Risk score: {summary['risk_score']}/100",
        f"- Alerts: {len(sorted_alerts)}",
        f"- High severity: {summary['severity_counts']['high']}",
        f"- Medium severity: {summary['severity_counts']['medium']}",
        "",
        "## Telemetry",
        "",
        f"- CPU load 1m: `{snapshot.get('cpu', {}).get('load_1m', 0)}`",
        f"- Memory used: `{snapshot.get('memory', {}).get('used_percent', 0)}%`",
        f"- Network interfaces: `{snapshot.get('network', {}).get('interface_count', 0)}`",
        f"- Established connections: `{len(snapshot.get('network', {}).get('connections', []))}`",
        f"- USB devices: {len(snapshot.get('usb', []))}",
        f"- Processes observed: {len(snapshot.get('processes', []))}",
        "",
        "## Priority Queue",
        "",
    ]
    if not sorted_alerts:
        lines.append("No immediate investigation queue was generated.")
    for index, alert in enumerate(sorted_alerts[:3], start=1):
        lines.append(f"{index}. **{alert['severity']}** - {alert['summary']} ({alert['kind']})")

    lines.extend(
        [
            "",
            "## Alerts",
            "",
        ]
    )
    if not sorted_alerts:
        lines.append("No alerts generated.")
    for alert in sorted_alerts:
        kind = str(alert["kind"])
        lines.extend(
            [
                f"### {alert['summary']}",
                "",
                f"- Severity: `{alert['severity']}`",
                f"- Type: `{kind}`",
                f"- Evidence: `{alert['evidence']}`",
                f"- Recommended next step: {NEXT_STEPS.get(kind, 'Review this alert with the original device snapshot.')}",
                "",
            ]
        )
    return "\n".join(lines) + "\n"


def build_timeline(snapshot: dict, alerts: list[dict]) -> str:
    """Return a compact timeline-style Markdown handoff."""
    lines = [
        "# DeviceWatch OS Alert Timeline",
        "",
        f"- Device: `{snapshot.get('device_id')}`",
        f"- Snapshot: {snapshot.get('captured_at')}",
        "",
        "## Events",
        "",
    ]
    if not alerts:
        lines.append("- No alert events generated.")
    for alert in sort_alerts(alerts):
        lines.append(f"- `{alert['severity']}` {alert['kind']}: {alert['summary']}")
    return "\n".join(lines).rstrip() + "\n"


def load_snapshot(path: Path) -> dict:
    """Load a telemetry snapshot."""
    return json.loads(path.read_text(encoding="utf-8"))


def write_outputs(snapshot: dict, alerts: list[dict], out_dir: Path) -> None:
    """Write MVP artifacts."""
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "snapshot.json").write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out_dir / "alerts.json").write_text(json.dumps(alerts, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out_dir / "dashboard-summary.json").write_text(
        json.dumps(build_dashboard_summary(snapshot, alerts), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (out_dir / "report.md").write_text(build_report(snapshot, alerts), encoding="utf-8")
    (out_dir / "alert-timeline.md").write_text(build_timeline(snapshot, alerts), encoding="utf-8")


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
