# Security Notes

DeviceWatch OS is defensive monitoring software. Use it only on devices, snapshots, and lab environments you own or have permission to assess.

## Data Handling

- Sample data uses documentation IP ranges and synthetic process names.
- Do not commit real device identifiers, access tokens, private logs, SSH keys, or customer telemetry.
- Treat process command lines as sensitive because they may include local paths or arguments.
- Redact hostnames and user names before sharing reports outside the trusted team.

## Agent Safety

- The current agent is read-only and does not kill processes, modify firewall rules, or change system state.
- Suspicious process and outbound connection alerts are triage signals, not proof of compromise.
- USB alerts should be compared with a known-good baseline before escalation.

## Future Production Controls

- Signed agent enrollment.
- Tenant-aware API authentication.
- TLS for telemetry upload.
- Retention policy for snapshots and reports.
- Baseline approval workflow with audit history.
