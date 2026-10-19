# Web Dashboard

The dashboard is a local Flask application implemented in `web/` with a Jinja template, JavaScript polling, and CSS.

## Displays

- Active alerts.
- Configured service status, operating mode, risk, and last event.
- CPU, RAM, and disk metrics.
- Recent events.

The browser refreshes service and event data from `/api/state` and `/api/events` every five seconds.

## Boundaries

The dashboard is read-only in this release. It does not issue restart requests or manage a separate task queue. Automatic recovery belongs to the engine's policy-controlled recovery path.

The built-in Flask development server is intended for local use, not direct internet exposure.