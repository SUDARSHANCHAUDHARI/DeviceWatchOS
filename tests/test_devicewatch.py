"""Tests for DeviceWatch OS MVP."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from agent.main import analyze_snapshot, build_dashboard_summary, build_report, build_timeline


ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data/samples/device-snapshot.json"


class DeviceWatchTests(unittest.TestCase):
    def test_analyzes_sample_snapshot(self) -> None:
        snapshot = json.loads(SAMPLE.read_text(encoding="utf-8"))

        alerts = analyze_snapshot(snapshot)
        kinds = {alert["kind"] for alert in alerts}

        self.assertIn("health.memory_high", kinds)
        self.assertIn("health.cpu_load_high", kinds)
        self.assertIn("health.reboot_recent", kinds)
        self.assertIn("security.suspicious_process", kinds)
        self.assertIn("security.unusual_outbound", kinds)
        self.assertIn("security.usb_present", kinds)

    def test_builds_report(self) -> None:
        snapshot = json.loads(SAMPLE.read_text(encoding="utf-8"))
        alerts = analyze_snapshot(snapshot)

        report = build_report(snapshot, alerts)

        self.assertIn("DeviceWatch OS Report", report)
        self.assertIn("kiosk-01", report)
        self.assertIn("Risk score", report)
        self.assertIn("Recommended next step", report)

    def test_builds_dashboard_summary_and_timeline(self) -> None:
        snapshot = json.loads(SAMPLE.read_text(encoding="utf-8"))
        alerts = analyze_snapshot(snapshot)

        summary = build_dashboard_summary(snapshot, alerts)
        timeline = build_timeline(snapshot, alerts)

        self.assertEqual(summary["device_id"], "kiosk-01")
        self.assertGreater(summary["risk_score"], 0)
        self.assertIn("DeviceWatch OS Alert Timeline", timeline)

    def test_cli_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "agent.main",
                    "--sample",
                    str(SAMPLE),
                    "--out-dir",
                    tmp,
                ],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertIn("Generated", result.stdout)
            self.assertTrue(Path(tmp, "alerts.json").exists())
            self.assertTrue(Path(tmp, "dashboard-summary.json").exists())
            self.assertTrue(Path(tmp, "alert-timeline.md").exists())
            self.assertTrue(Path(tmp, "report.md").exists())


if __name__ == "__main__":
    unittest.main()
