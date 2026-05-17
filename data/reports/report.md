# DeviceWatch OS Report

- Device: `kiosk-01`
- Captured: 2026-05-17T10:00:00+00:00
- Alerts: 4

## Telemetry

- CPU: `{'cpu_count': 2, 'load_15m': 1.2, 'load_1m': 5.5, 'load_5m': 2.1}`
- Memory: `{'available_kb': 102400, 'total_kb': 2048000, 'used_percent': 95.0}`
- Network: `{'interface_count': 2, 'interfaces': [{'name': 'eth0', 'rx_bytes': 10000, 'tx_bytes': 5000}]}`
- USB devices: 1

## Alerts

### Memory usage is above the configured threshold.

- Severity: `high`
- Type: `health.memory_high`
- Evidence: `{'available_kb': 102400, 'total_kb': 2048000, 'used_percent': 95.0}`

### One-minute CPU load is unusually high for this device.

- Severity: `medium`
- Type: `health.cpu_load_high`
- Evidence: `{'cpu_count': 2, 'load_15m': 1.2, 'load_1m': 5.5, 'load_5m': 2.1}`

### Process command line matches a suspicious pattern.

- Severity: `high`
- Type: `security.suspicious_process`
- Evidence: `{'args': 'python reverse tunnel client', 'command': 'python', 'pid': '777', 'user': 'kiosk'}`

### USB devices are present and should be checked against the expected baseline.

- Severity: `low`
- Type: `security.usb_present`
- Evidence: `{'usb_count': 1}`

