# DeviceWatch OS

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](#requirements)
[![Status](https://img.shields.io/badge/status-MVP-green)](#status)
[![Security](https://img.shields.io/badge/security-defensive%20lab-purple)](#safe-use)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Security and health monitoring agent for Linux devices, kiosks, digital signage players, and edge systems. Collects CPU, memory, network, processes, and USB telemetry into a structured snapshot for analysis.

---

## Overview

DeviceWatch OS is a defensive monitoring agent that runs locally on a Linux device and captures a security-relevant snapshot: CPU/memory pressure, network connections, running processes, USB device list, and OS metadata. The snapshot is written as JSON for downstream analysis or shipped to a central collector. Useful for fleet operators managing kiosks, signage, and unattended Linux devices.

The current MVP is a Python CLI agent. A FastAPI + React management dashboard is scaffolded under `apps/` for future development.

## Features

- Collects CPU and memory usage
- Lists network interfaces and active connections
- Enumerates running processes with command lines
- Lists connected USB devices
- Captures OS, hostname, and kernel metadata
- Writes structured JSON snapshot for offline analysis
- Builds Markdown summary and dashboard JSON

## Requirements

- Python 3.10 or newer
- Linux (full feature support); macOS / Windows (partial)
- No third-party Python packages (standard library only)
- Optional: Docker for the demo container

## Installation

```bash
git clone https://github.com/SUDARSHANCHAUDHARI/DeviceWatchOS.git
cd DeviceWatchOS
pip install .
```

This registers the `device-watch` CLI command.

To run without installing:

```bash
python3 main.py --help
```

## Usage

Capture a device snapshot using the bundled sample data:

```bash
python3 main.py --sample data/samples/device-snapshot.json --out-dir reports
```

Generated outputs in `reports/`:

- `snapshot.json` — raw collected telemetry
- `summary.json` — dashboard-friendly summary
- `report.md` — Markdown health and security report

## Project Structure

```
DeviceWatchOS/
├── agent/          Telemetry collectors and snapshot builder
│   ├── collectors/ CPU, memory, network, processes, USB
│   └── main.py     Agent entry
├── apps/
│   ├── api/        FastAPI app scaffold (planned)
│   └── web/        React/Next.js app scaffold (planned)
├── data/           Safe sample snapshots
├── docker/         Dockerfile + compose support
├── docs/           Architecture, security, demo notes
├── scripts/        Setup, seed, run helpers
├── tests/          Unit and integration tests
├── main.py         CLI entrypoint
├── pyproject.toml  Package metadata
└── LICENSE
```

## Testing

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

## Docker Demo

```bash
docker compose run --rm api
```

## Safe Use

This project is defensive and analysis-focused. Run only on devices and lab environments you own or have explicit written permission to monitor.

## Status

Working Python CLI agent MVP. Web dashboard scaffold present but not yet implemented.

## Roadmap

- Live snapshot mode reading real `/proc`, `/sys`, and `lsusb`
- Baseline diffing across snapshots
- Scheduled snapshot uploads to a central collector
- Web dashboard for fleet health
- TLS-secured snapshot ingest API

## License

Released under the [MIT License](LICENSE). You are free to use, modify, and distribute this software with attribution.

## Author

**Sudarshan Chaudhari** — [SudarshanTechLabs](https://github.com/SUDARSHANCHAUDHARI)
Bangkok, Thailand

For inquiries: open an issue on [GitHub](https://github.com/SUDARSHANCHAUDHARI/DeviceWatchOS/issues).
