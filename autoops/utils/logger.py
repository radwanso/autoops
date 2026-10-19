import json
from datetime import datetime

LOG_FILE = "autoops.log"


def log_event(message):
    entry = {
        "time": datetime.now().isoformat(),
        "message": message
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")


def load_logs(limit=50):
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()[-limit:]

        return [json.loads(line) for line in reversed(lines)]

    except FileNotFoundError:
        return []

