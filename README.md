# DeviceWatch OS

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](#requirements)
[![Status](https://img.shields.io/badge/status-MVP-green)](#status)
[![Security](https://img.shields.io/badge/security-defensive%20lab-purple)](#safe-use)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Security and health monitoring agent for Linux devices, kiosks, digital signage players, and edge systems. Collects CPU, memory, network, processes, and USB telemetry into a structured snapshot for analysis.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Docker Demo](#docker-demo)
- [Safe Use](#safe-use)
- [Status](#status)
- [Roadmap](#roadmap)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [About](#about)

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

## Documentation

Full project documentation lives in [`docs/`](docs/):

- [Architecture](docs/ARCHITECTURE.md) — component design and data flow
- [Demo](docs/DEMO.md) — step-by-step demo walkthrough
- [Security Notes](docs/SECURITY_NOTES.md) — defensive-use guidance and threat model
- [Production Readiness](docs/PRODUCTION_READINESS.md) — gaps between MVP and production
- [Project Plan](docs/PROJECT_PLAN.md) — scope and milestones
- [Roadmap](docs/ROADMAP.md) — planned features
- [Release Notes](docs/RELEASE_NOTES.md) — version history

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) and the [Code of Conduct](CODE_OF_CONDUCT.md) before opening a pull request. To report a security issue, see [SECURITY.md](SECURITY.md).

## License

Released under the [MIT License](LICENSE). You are free to use, modify, and distribute this software with attribution.

---

## About

I'm Sudarshan Chaudhari, a Senior Quality Engineer, Test Automation specialist, and AI systems builder based in Bangkok, Thailand.

I have 13+ years of experience in software quality engineering, working across SaaS, fintech, gaming, web, mobile, cloud, and digital signage platforms. My background combines hands-on test automation with QA leadership, test strategy, CI/CD, release quality, production investigation, and cross-platform validation.

Alongside my professional QA career, I run [SudarshanTechLabs](https://sudarshantechlabs.com/), my independent engineering and product lab where I design, build, test, and ship software across Android, web, AI, cybersecurity, developer tooling, and cross-platform applications.

### What I work on

- ⚙️ **Quality Engineering & Test Automation** — Playwright, Selenium, Cypress, Appium, API testing, automation frameworks, end-to-end testing, CI/CD, release gates, GitHub Actions, risk-based testing, and production validation
- 🤖 **AI Systems & Automation** — AI agents, multi-agent orchestration, MCP servers, AI-assisted QA, prompt tooling, developer workflows, automation systems, and Claude Code plugins
- 📱 **Mobile & Cross-Platform Applications** — Android applications built with Kotlin and Jetpack Compose, Google Play releases, automated build and publishing pipelines, and cross-platform development spanning iOS, web, Windows, and macOS
- 🌐 **Web Applications & Platforms** — Full-stack applications using Next.js, TypeScript, Firebase, Cloudflare, REST APIs, and modern web infrastructure
- 🛠️ **Developer Tooling & CLI Engineering** — Rust, Python, TypeScript, CLI utilities, multi-repository tooling, build automation, release tooling, and engineering productivity systems
- 🛡️ **Cybersecurity & Observability** — Threat detection, log analysis, security auditing, vulnerability assessment, monitoring, and security-focused developer tools
- 📺 **Digital Signage & Device Platforms** — Content validation, playback testing, device compatibility, production investigation, monitoring, and QA across diverse hardware and operating-system environments

My work sits at the intersection of quality engineering, automation, AI, and software development. I approach products with a QA mindset from the beginning: understanding failure modes, designing for testability, automating repetitive work, and building release confidence into the engineering process.

Through SudarshanTechLabs, I also build products and tools from idea to production, covering architecture, development, testing, CI/CD, release automation, monitoring, and ongoing maintenance.

🌐 [sudarshantechlabs.com](https://sudarshantechlabs.com/) · 💼 [LinkedIn](https://linkedin.com/in/sudarshan-chaudhari) · 🐙 [GitHub](https://github.com/SUDARSHANCHAUDHARI) · ✉️ [sunny.sudarshan@gmail.com](mailto:sunny.sudarshan@gmail.com)
