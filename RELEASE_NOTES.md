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
- The owner verified this v8 candidate on Ubuntu 24.04 under WSL2: the combined launcher/dashboard ran, Telegram delivered alerts, and stopping nginx led to `RESTART_SENT` (rc=0) followed by an active service.
- The repeated-stop test exposed a permanent-lockout behavior; the v8 recovery guard was updated and then verified with a subsequent successful recovery.
