# AutoOps Project Status

## Release status

The canonical runtime was exercised on Ubuntu 24.04 under WSL2. The v7 packaging pass removed unconnected legacy paths and corrected the dashboard/API scope. The v8 recovery pass fixes a permanent escalation lockout after repeated outages and resets the active failure streak after a monitored recovery. The owner verified Telegram alerts and nginx recovery with `RESTART_SENT` (rc=0), followed by an active service.

## Verified behavior

- `python -m autoops.start` starts the engine and dashboard together and shuts both down on Ctrl+C.
- The configured nginx, cron, and ssh services were reported UP while healthy.
- Socket-activated SSH is considered UP while `ssh.socket` is active.
- A simulated failure of a temporary systemd unit passed through policy, decision, and recovery execution; the unit returned to active.
- Non-root recovery uses `sudo -n` and was verified with a narrowly scoped sudoers rule.
- The dashboard displayed service status, risk, metrics, and normalized events.
- Python source compilation and targeted recovery-policy checks passed for this v8 candidate.
- Mocked checks cover Telegram delivery success, API rejection, request failure, missing credentials, and the 60-second repeat cooldown.
- Telegram notification delivery has a timeout and checks Telegram's API success response. The owner confirmed actual Telegram delivery and automatic outage alerts on the target WSL host.

## Supported scope

- One Linux host with systemd.
- Local JSON persistence under `autoops/data/`.
- Policy-controlled systemd restart recovery.
- Local monitoring dashboard on port 5000.

## Explicit limitations

- The Flask development server is for local use and is not configured for internet exposure.
- Manual recovery from the dashboard is not included; the dashboard is read-only.
- The optional systemd installation manages the engine only and must not run alongside the combined local launcher.
- Docker, distributed hosts, external databases, and a production web server are outside this release.

## Closure

No additional features are required to close this version. Future work should begin only from a concrete need observed during use.
