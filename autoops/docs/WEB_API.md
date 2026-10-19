# AutoOps Web API

The local Flask application exposes read-only monitoring data.

| Method | Path | Purpose |
|---|---|---|
| GET | `/` | Dashboard page. |
| GET | `/health` | Basic web-process health response. |
| GET | `/api/state` | Configured services, service status/risk, system metrics, and alerts. |
| GET | `/api/events` | Recent normalized event records. |
| GET | `/api/timeline` | Recent events formatted as timeline messages. |

The dashboard does not accept manual recovery requests in this release. Recovery decisions and systemd restarts are handled by the canonical engine path.