# Troubleshooting

## Port 5000 is already in use

A dashboard process is already listening. Reuse its browser page or stop the old dashboard from the terminal where it was started before launching `python -m autoops.start` again. Do not start a second engine.

## A service appears DOWN

Check the unit with `systemctl is-active <unit>`. For socket-activated services such as SSH, also check the corresponding socket unit (for example `ssh.socket`). AutoOps reports SSH as available when its socket is active.

## Recovery requires authentication

For a non-root AutoOps process, recovery uses `sudo -n`. Confirm the `/etc/sudoers.d/autoops-recovery` rule grants only the exact restart commands for configured services, then validate it with `sudo visudo -cf /etc/sudoers.d/autoops-recovery`.

## Dashboard data looks stale

Confirm the engine is running and that `/api/state` and `/api/events` return HTTP 200. Refresh the page after restarting the combined launcher.

For supported scope and run instructions, see [`../README.md`](../../README.md) and [`DEPLOYMENT.md`](DEPLOYMENT.md).