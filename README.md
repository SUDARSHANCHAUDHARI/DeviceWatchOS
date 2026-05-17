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
- Flags suspicious process command lines.
- Flags USB presence for baseline review.
- Writes JSON snapshots, JSON alerts, and a Markdown device report.

## Roadmap

- Polish sample output screenshots or terminal demos
- Add architecture diagram and deeper implementation notes
- Expand test coverage around edge cases
- Add Docker or local demo workflow where useful
- Prepare `v0.1.0-mvp` release notes
