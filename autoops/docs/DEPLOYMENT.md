# Deployment and Local Operation

## Requirements

- Linux with systemd enabled (tested with Ubuntu 24.04 on WSL2).
- Python 3.10 or newer.
- Packages in `autoops/requirements.txt`.
- `systemctl` access for monitoring.

## Install

Run from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r autoops/requirements.txt
```

## Configure Telegram alerts

Telegram is optional. In the WSL terminal you will use to start AutoOps, enter the bot token without echoing it and enter the destination chat ID:

```bash
read -rsp 'Telegram bot token: ' TELEGRAM_TOKEN; echo
read -rp 'Telegram chat ID: ' TELEGRAM_CHAT_ID
export TELEGRAM_TOKEN TELEGRAM_CHAT_ID
python -m autoops.actions.notifier --test
```

The test command sends one message and exits nonzero if configuration or delivery fails. Do not paste the bot token into chat or commit it to GitHub. Keep this terminal session open and start AutoOps in the same session so it inherits the variables.

Only HIGH or CRITICAL risk triggers alert messages. A message is sent on detection and repeated every 60 seconds while the same service/risk/running condition continues. The engine checks every five seconds but does not send on every tick. Telegram delivery needs network access from the WSL host.

## Allow narrowly scoped recovery

When AutoOps runs as a regular user, its executor uses non-interactive sudo for approved systemd restarts. Grant only the exact restart commands for services configured in `autoops/config/config.yaml`. Example:

```sudoers
radwan ALL=(root) NOPASSWD: /bin/systemctl restart nginx, /bin/systemctl restart cron, /bin/systemctl restart ssh
```

Replace `radwan` and the unit names if needed. Save the rule to `/etc/sudoers.d/autoops-recovery`, set mode `0440`, and validate it:

```bash
sudo chmod 0440 /etc/sudoers.d/autoops-recovery
sudo visudo -cf /etc/sudoers.d/autoops-recovery
```

This grants only the listed restart operations, not general root access.

## Start

From the repository root with the virtual environment active and, if used, Telegram variables set:

```bash
python -m autoops.start
```

The launcher starts the engine and dashboard. Open `http://localhost:5000`; press `Ctrl+C` to stop both. Do not start a second engine while this launcher or the optional systemd engine service is running.

## Optional systemd engine service

`python -m autoops.cli install` manages the engine only, not the dashboard. It is separate from `python -m autoops.start`. Shell environment variables are not automatically passed to this systemd service in this release; use the combined launcher for the documented Telegram setup.

## Runtime files and boundaries

Runtime state, memory, and events are written as JSON under `autoops/data/`. Keep this directory when updating code; generated runtime data is excluded from source archives.

AutoOps monitors one local Linux host. The built-in Flask server is for local use, not direct internet exposure. Docker, distributed monitoring, and external databases are outside this release.