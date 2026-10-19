import json
import os
import time

EVENTS_FILE = "autoops/data/events.json"


def log_event(service, event, decision=None, details=None):

    # The engine historically passed the event name as the first argument and
    # a payload dictionary as the second. Normalize that form to the same
    # schema used by service actions so the dashboard never receives an
    # object in its display fields.
    if isinstance(event, dict):
        event_name = service
        payload = event
        service = payload.get("service", "system")
        if decision is None:
            decision = payload.get("decision")
        if details is None:
            details = payload
        event = event_name

    os.makedirs("autoops/data", exist_ok=True)

    if os.path.exists(EVENTS_FILE):
        with open(EVENTS_FILE, "r") as f:
            try:
                events = json.load(f)
            except:
                events = []
    else:
        events = []

    new_event = {
        "time": time.time(),
        "service": service,
        "event": event,
        "decision": decision,
        "details": details
    }

    events.append(new_event)

    # keep last 500 events only
    events = events[-500:]

    with open(EVENTS_FILE, "w") as f:
        json.dump(events, f, indent=2)
