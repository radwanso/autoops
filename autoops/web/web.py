from flask import (
    Flask,
    jsonify,
    render_template
)

import json
import os

from datetime import datetime

from autoops.core.config import load_config
from autoops.core.monitor import get_system_metrics, is_service_running

# =========================
# Flask App
# =========================

app = Flask(
    __name__,
    template_folder="templates"
)


# =========================
# Paths
# =========================

BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

STATE_FILE = os.path.join(
    DATA_DIR,
    "state.json"
)

EVENTS_FILE = os.path.join(
    DATA_DIR,
    "events.json"
)


# =========================
# Safe JSON Loader
# =========================

def safe_load_json(path, default):

    try:

        if os.path.exists(path):

            with open(path) as f:
                return json.load(f)

    except Exception as e:

        print(f"[WEB LOAD ERROR] {path}: {e}")

    return default


# =========================
# API: STATE
# =========================

@app.route("/api/state")
def api_state():

    state = safe_load_json(
        STATE_FILE,
        {}
    )

    stored_system = state.get("_system", {})
    try:
        live_metrics = get_system_metrics()
    except Exception as e:
        print(f"[SYSTEM METRICS ERROR] {e}")
        live_metrics = {}

    system = {
        "cpu": stored_system.get("cpu", live_metrics.get("cpu")),
        "ram": stored_system.get("ram", live_metrics.get("memory")),
        "disk": stored_system.get("disk", live_metrics.get("disk")),
    }

    services = []
    alerts = []
    configured = load_config().get("services", []) or []
    configured_names = [
        item.get("name") for item in configured
        if isinstance(item, dict) and item.get("name")
    ]
    service_names = configured_names + [
        name for name in state
        if name != "_system" and name not in configured_names
    ]

    for name in service_names:
        data = state.get(name, {})
        if not data:
            running = is_service_running(name)
            data = {
                "status": "UP" if running else "DOWN",
                "mode": "NORMAL",
                "risk": "UNKNOWN",
                "history": [],
            }

        risk = data.get("risk", "LOW")
        if isinstance(risk, dict):
            risk = risk.get("level", "UNKNOWN")

        history = data.get("history", [])
        last_event = data.get("last_event")
        if not last_event and history:
            last_event = history[-1].get("event", "NONE")

        status = data.get("status", "DOWN")

        # ========================
        # ALERTS
        # ========================

        if status != "UP" or risk in ("HIGH", "CRITICAL"):

            alerts.append({

                "service": name,
                "status": status,

                "risk": risk,
                "event": last_event or "NONE"
            })

        # =============================
        # SERVICES
        # =============================

        services.append({

            "name": name,

            "status": data.get(
                "status",
                "DOWN"
            ),

            "mode": data.get(
                "mode",
                "NORMAL"
            ),

            "risk": risk,

            "last_event": last_event or "NONE",

            "strategy": data.get(
                "strategy",
                "NORMAL"
            )
        })

    return {
        "system": system,
        "services": services,
        "alerts": alerts
    }


# =========================
# API: EVENTS
# =========================

@app.route("/api/events")
def api_events():

    events = safe_load_json(
        EVENTS_FILE,
        []
    )

    normalized = []
    for raw_event in events[-50:]:
        if not isinstance(raw_event, dict):
            continue

        event_name = raw_event.get("event", "event")
        service = raw_event.get("service", "system")
        decision = raw_event.get("decision")

        # Support old engine log records where the event name was written to
        # `service` and the `event` field contains the complete payload.
        if isinstance(event_name, dict):
            payload = event_name
            event_name = service
            service = payload.get("service", "system")
            decision = decision or payload.get("decision")

        if isinstance(event_name, (dict, list)):
            event_name = "event"
        if isinstance(service, (dict, list)):
            service = "system"
        if isinstance(decision, (dict, list)):
            decision = "—"

        normalized.append({
            "time": raw_event.get("time"),
            "service": service,
            "event": event_name,
            "decision": decision,
        })

    return jsonify(normalized)

# =========================
# =
# =========================
@app.route("/api/timeline")
def api_timeline():

    events = safe_load_json(
        EVENTS_FILE,
        []
    )

    timeline = []

    for e in events:

        timeline.append({

            "time": e.get("time"),

            "message":
                f"{e.get('service', 'system')} "
                f"{e.get('event', 'event')} → "
                f"{e.get('decision') or '—'}"

        })

    timeline.sort(
        key=lambda x: x["time"],
        reverse=True
    )

    return timeline[:30]

# =========================
# HEALTHY CHECK
# =========================
@app.route("/health")
def health():

    return {
        "status": "healthy"
    }

# =========================
# Dashboard
# =========================

@app.route("/")
def index():

    state = safe_load_json(
        STATE_FILE,
        {}
    )

    events = safe_load_json(
        EVENTS_FILE,
        []
    )

    system_data = state.get("_system", {
        "cpu": 0,
        "ram": 0,
        "disk": 0,
        "health": "UNKNOWN"
    })

    services = []

    system_data = state.get("_system", {})

    for name, data in state.items():

        if name == "_system":
            continue

        attempts = data.get(
            "restart_attempts",
            0
        )

        success = data.get(
            "success_count",
            0
        )

        fail_count = data.get(
            "fail_count",
            0
        )

        status = data.get(
            "status",
            "DOWN"
        )

        # =========================
        # Success Rate
        # =========================

        if status != "UP":

            success_rate = 0

        elif attempts > 0:

            success_rate = round(
                (success / attempts) * 100,
                1
            )

        else:

            success_rate = 100

        # =========================
        # Health Score
        # =========================

        if status != "UP":

            health = 0

        else:

            health = max(
                0,
                100
                - (fail_count * 15)
                - (attempts * 5)
            )

        # =========================
        # Stability
        # =========================

        if health >= 80:

            stability = "Stable"

        elif health >= 50:

            stability = "Warning"

        elif health >= 30:

            stability = "Unstable"

        else:

            stability = "Critical"

        services.append({

            "name": name,

            "status": status,

            "health": health,

            "stability": stability,

            "fail_count": fail_count,

            "restart_attempts": attempts,

            "strategy": data.get(
                "strategy",
                "NORMAL"
            ),

            "last_event": data.get(
                "last_event",
                "NONE"
            ),

            "reputation": data.get(
                "reputation",
                0
            ),

            "mode": data.get(
                "mode",
                "NORMAL"
            )

        })

    # =========================
    # Format Events
    # =========================

    for event in events:

        try:

            event["formatted_time"] = (
                datetime.fromtimestamp(
                    event["time"]
                ).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )

        except Exception:

            event["formatted_time"] = "UNKNOWN"

    return render_template(

        "index.html",


        state=state,
        services=services,
        system=system_data,
        events=events[-20:]
    )


# =========================
# Main
# =========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )
