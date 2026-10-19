# Telegram Alerts

## Configure and send one test

Set `TELEGRAM_TOKEN` and `TELEGRAM_CHAT_ID` in the same WSL shell used to launch AutoOps. The safe interactive setup and one-message test are in [`DEPLOYMENT.md`](DEPLOYMENT.md). Never commit or paste the bot token.

The sender reads the environment at send time, applies a finite HTTP timeout, checks HTTP status and Telegram's JSON `ok` result, and reports success/failure without printing the token.

## Alert and repeat behavior

- The engine sends Telegram alerts only when risk is HIGH or CRITICAL.
- It enforces a 60-second cooldown per service/risk/running condition; the reminder is sent on the next five-second engine tick after the cooldown expires.
- If the condition remains, reminders continue at that interval until the risk clears or the engine stops.
- It does not send every five-second engine tick.
- Cooldown timestamps are held in memory and reset when the engine restarts. This release does not send a separate recovery/resolved message.
- A test run with `python -m autoops.actions.notifier --test` sends exactly one message and does not stop or restart a service.

## Verification boundary

Compilation and alert-path code can be checked without credentials. Actual delivery must be verified on the user's WSL host with the private bot token and chat ID; keep those values local.
