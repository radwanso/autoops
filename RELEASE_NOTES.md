# AutoOps release candidate v8

This is a packaging revision for the local single-host AutoOps project, not a claim of production deployment.

## Included

- Canonical monitor, policy, decision, and systemd recovery path.
- Local Flask dashboard and read-only monitoring API.
- Scoped non-root restart setup instructions.
- Updated architecture, API, deployment, and project status documentation.
- Telegram alerts repeat after a 60-second cooldown for persistent HIGH/CRITICAL conditions; the sender now checks Telegram's API response and uses a request timeout.
- Added a one-message Telegram delivery test command.
- Recovery safeguards now allow one conservative restart attempt for a confirmed outage, count actual restart commands, and clear the active failure streak after the service is observed UP. Historical events remain available for diagnostics.

## Cleanup

- Removed the unused agent and its separate task queue.
- Removed the unreferenced legacy pipeline and controller backup.
- Removed action helpers and the dashboard `/fix` path that queued requests with no active worker.
- Removed the empty task-history section; recovery events remain visible in the event timeline.

## Verification

- Python compilation passed for this v8 candidate. Targeted policy checks confirm one conservative attempt is allowed and further attempts escalate; a pipeline state check confirms a recovered service clears its active failure streak.
- Mocked sender and alert-cooldown checks passed; they do not replace a real bot delivery test.
- The v5 baseline was exercised on Ubuntu 24.04 under WSL2: stable monitoring, recovery through a temporary unit, dashboard API/UI, and graceful launcher shutdown.
- The owner confirmed an actual Telegram test message and automatic outage alerts were delivered. A real recovery attempt was also observed in the WSL log (`RESTART_SENT`, rc=0); the repeated-stop case exposed the permanent-lockout behavior corrected in this v8 candidate.
- Re-run the Telegram one-message check and combined launcher/dashboard check on the extracted candidate before tagging it on GitHub. The Codex host used to prepare this archive does not have the WSL/systemd service available for that final host-specific check.
