# DeviceWatch OS Report

- Device: `kiosk-01`
- Captured: 2026-05-17T10:00:00+00:00
- Heartbeat: `online`
- Risk score: 100/100
- Alerts: 6
- High severity: 3
- Medium severity: 2

## Telemetry

- CPU load 1m: `5.5`
- Memory used: `95.0%`
- Network interfaces: `2`
- Established connections: `1`
- USB devices: 1
- Processes observed: 2

## Priority Queue

1. **high** - Memory usage is above the configured threshold. (health.memory_high)
2. **high** - Process command line matches a suspicious pattern. (security.suspicious_process)
3. **high** - Established outbound connection uses a port that should be reviewed. (security.unusual_outbound)

## Alerts

### Memory usage is above the configured threshold.

- Severity: `high`
- Type: `health.memory_high`
- Evidence: `{'available_kb': 102400, 'total_kb': 2048000, 'used_percent': 95.0}`
- Recommended next step: Inspect memory-heavy processes and restart the kiosk workload only after preserving telemetry.

### Process command line matches a suspicious pattern.

- Severity: `high`
- Type: `security.suspicious_process`
- Evidence: `{'args': 'python reverse tunnel client', 'command': 'python', 'pid': '777', 'user': 'kiosk'}`
- Recommended next step: Quarantine the process, capture command-line evidence, and compare against the approved image.

### Established outbound connection uses a port that should be reviewed.

- Severity: `high`
- Type: `security.unusual_outbound`
- Evidence: `{'local_address': '10.10.20.15', 'local_port': 49152, 'remote_address': '198.51.100.77', 'remote_port': 4444, 'state': 'ESTABLISHED'}`
- Recommended next step: Validate the destination IP and port against expected device egress rules.

### Device rebooted recently and should be checked against the expected maintenance window.

- Severity: `medium`
- Type: `health.reboot_recent`
- Evidence: `{'uptime_seconds': 420, 'status': 'online'}`
- Recommended next step: Confirm the reboot matches a maintenance window or known power event.

### One-minute CPU load is unusually high for this device.

- Severity: `medium`
- Type: `health.cpu_load_high`
- Evidence: `{'cpu_count': 2, 'load_15m': 1.2, 'load_1m': 5.5, 'load_5m': 2.1}`
- Recommended next step: Check process list, recent deployments, and browser rendering loops before rebooting.

### USB devices are present and should be checked against the expected baseline.

- Severity: `low`
- Type: `security.usb_present`
- Evidence: `{'usb_count': 1}`
- Recommended next step: Compare attached USB devices against the baseline for this location.

