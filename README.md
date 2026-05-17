# DeviceWatch OS

**Goal:** Security and health monitoring for remote devices.

**MVP:** Agent sends device metrics to dashboard.

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

## Repository Status

This repository contains the production-ready foundation for the DeviceWatch OS MVP. The current codebase is scaffolded and ready for focused implementation work.

## Production Foundation

- Private GitHub repository linked to `main`
- Initial MVP scaffold committed
- CI repository-health workflow
- Security policy
- Contribution guide
- Pull request and issue templates
- Production readiness checklist
- Safe ignore rules for local secrets and generated files
