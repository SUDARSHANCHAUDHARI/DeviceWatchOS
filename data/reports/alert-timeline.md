# DeviceWatch OS Alert Timeline

- Device: `kiosk-01`
- Snapshot: 2026-05-17T10:00:00+00:00

## Events

- `high` health.memory_high: Memory usage is above the configured threshold.
- `high` security.suspicious_process: Process command line matches a suspicious pattern.
- `high` security.unusual_outbound: Established outbound connection uses a port that should be reviewed.
- `medium` health.reboot_recent: Device rebooted recently and should be checked against the expected maintenance window.
- `medium` health.cpu_load_high: One-minute CPU load is unusually high for this device.
- `low` security.usb_present: USB devices are present and should be checked against the expected baseline.
