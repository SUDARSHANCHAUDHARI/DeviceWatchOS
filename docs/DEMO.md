# Demo

Run the sample device snapshot through the agent:

```bash
python3 -m agent.main --sample data/samples/device-snapshot.json --out-dir data/reports
```

Expected output:

```text
Device: kiosk-01
Generated 6 alert(s)
```

Generated artifacts:

- `data/reports/snapshot.json`
- `data/reports/alerts.json`
- `data/reports/dashboard-summary.json`
- `data/reports/report.md`
- `data/reports/alert-timeline.md`

The sample highlights a kiosk-style device with high memory use, high CPU load, recent reboot, suspicious process arguments, unusual outbound connection, and USB review signal.
