# AutoOps

AutoOps monitors configured Linux systemd services, evaluates their state and risk, and can restart an approved service when recovery policy allows it. A local Flask dashboard displays service status, system metrics, alerts, and recent events.

This release is intended for local use on one Linux host. It was exercised on Ubuntu 24.04 under WSL2 with systemd enabled.

## Requirements

- Linux with systemd enabled
- Python 3.10 or newer
- Packages in `autoops/requirements.txt`

## Install

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r autoops/requirements.txt
```

## Configure recovery permissions

AutoOps can run as a regular user. For automatic restarts, grant narrowly scoped permission only for the systemd units listed in `autoops/config/config.yaml`. For example, replace `radwan` if needed:

```sudoers
radwan ALL=(root) NOPASSWD: /bin/systemctl restart nginx, /bin/systemctl restart cron, /bin/systemctl restart ssh
```

Save the rule in `/etc/sudoers.d/autoops-recovery`, set mode `0440`, and validate it with `visudo -cf`. Do not grant general sudo access to AutoOps.

## Run

Start the engine and dashboard together:

```bash
source .venv/bin/activate
python -m autoops.start
```

Open <http://localhost:5000>. Press `Ctrl+C` in the terminal to stop both processes. Do not run a second engine or another dashboard on port 5000 at the same time.

## Telegram alerts

Set `TELEGRAM_TOKEN` and `TELEGRAM_CHAT_ID` in the same WSL terminal before starting AutoOps. To test delivery, run `python -m autoops.actions.notifier --test`; it sends exactly one test message. Do not paste the bot token into chat or commit it to GitHub.

The engine sends alerts for `HIGH` or `CRITICAL` risk and repeats after a 60-second cooldown, on the next five-second engine tick, while that same service condition remains. It does not send a message on every tick. See `autoops/docs/TELEGRAM.md` for setup and behavior.

## Scope and limitations

- Monitors services on the local host only.
- Stores runtime state as local JSON under `autoops/data/`; that generated data is excluded from the source repository.
- Uses Flask's development server for local access. It is not configured for direct internet exposure.
- Dashboard is for monitoring; manual recovery requests are not part of this release.
- The supported recovery path is the engine's policy-controlled systemd restart flow.
- Optional systemd installation through `python -m autoops.cli install` manages the engine only. Do not use it at the same time as `python -m autoops.start`.

See `autoops/docs/DEPLOYMENT.md` and `autoops/PROJECT_STATUS.md` for operational details and the verified project status.
