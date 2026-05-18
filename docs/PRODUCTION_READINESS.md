# Production Readiness

## Current Status

This repository has a working local MVP with deterministic analysis, safe sample data, generated reports, and tests. It is not production complete yet.

## Required Before Public Release

- Add signed agent enrollment and authenticated API ingestion.
- Validate all uploaded snapshots and reject unknown schema versions.
- Add structured logging without leaking secrets.
- Store telemetry in PostgreSQL with retention controls.
- Add authentication and authorization before multi-device dashboard usage.
- Add baseline approval and suppression audit logs.
- Package the agent with least-privilege install instructions.
- Run dependency and secret scans before release.

## Definition of Done

- CI passes on pull requests.
- README has setup, usage, and security notes.
- Sample data is safe to publish.
- Error paths are handled clearly.
- No secrets or local machine paths are committed.
