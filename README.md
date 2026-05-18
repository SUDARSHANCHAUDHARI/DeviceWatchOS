# DeviceWatch OS

[![Python](https://img.shields.io/badge/Python-3.12-blue)](#) [![Status](https://img.shields.io/badge/status-MVP-green)](#) [![Security](https://img.shields.io/badge/security-defensive%20lab-purple)](#)

Security and health monitoring MVP for Linux devices, kiosks, signage players, and edge systems.

- **Portfolio group:** Product-style SaaS project
- **Status:** MVP implemented, tested, committed, and pushed to GitHub
- **GitHub:** https://github.com/SUDARSHANCHAUDHARI/DeviceWatchOS
- **Local path:** `/Users/screencloudsudarshan/SUDARSHAN_CODE/sudarshan_repos/CyberSecurity/DeviceWatchOS`

## MVP Snapshot

This repository includes a working MVP with safe sample data, deterministic detection or analysis logic, local tests, and generated output reports where relevant. It is ready for README/demo polish or deeper product work.

## Safe Use

This project is defensive and analysis-focused. Use only with logs, systems, repositories, and lab environments you own or have permission to assess.

## Core Features

- device heartbeat
- reboot tracking
- CPU/RAM/network usage
- suspicious process detection
- USB event detection
- alert dashboard

## Suggested Stack

Python agent, FastAPI, React, PostgreSQL, Docker.

## Status

Working CLI MVP.

## Quick Start

Analyze the included sample snapshot:

```bash
python3 -m agent.main --sample data/samples/device-snapshot.json --out-dir data/reports
```

Collect and analyze the local machine:

```bash
python3 -m agent.main --out-dir data/reports
```

Run tests:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

## MVP Capabilities

- Collects local heartbeat, CPU, memory, network, process, and USB telemetry.
- Analyzes high memory usage and unusual CPU load.
- Flags recent reboot signals for maintenance-window review.
- Flags suspicious process command lines.
- Flags suspicious established outbound connections.
- Flags USB presence for baseline review.
- Builds a dashboard summary with risk score and severity counts.
- Writes JSON snapshots, alerts, dashboard summary, device report, and alert timeline.

## Demo Artifacts

- [Architecture](docs/ARCHITECTURE.md)
- [Security notes](docs/SECURITY_NOTES.md)
- [Production readiness](docs/PRODUCTION_READINESS.md)
- [Sample device report](data/reports/report.md)
- [Sample alert timeline](data/reports/alert-timeline.md)
- [Sample dashboard summary](data/reports/dashboard-summary.json)

## Docker Demo

```bash
docker compose run --rm devicewatch-demo
```

## Roadmap

- Add signed agent enrollment and per-device baseline approval.
- Add FastAPI ingestion routes backed by PostgreSQL.
- Add React dashboard for fleet health, alert timeline, and device detail views.
- Add policy packs for kiosk, signage player, Raspberry Pi, and Linux server profiles.
- Prepare GitHub release `v0.1.0-mvp`.
