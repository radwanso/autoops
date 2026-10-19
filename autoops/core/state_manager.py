import json
import os
import threading

STATE_FILE = "autoops/data/state.json"
lock = threading.Lock()


def _ensure_file():
    if not os.path.exists(STATE_FILE):
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        with open(STATE_FILE, "w") as f:
            json.dump({}, f)


def get_state():
    with lock:
        _ensure_file()
        try:
            with open(STATE_FILE, "r") as f:
                data = json.load(f)

                # 🔥 FORCE SAFE TYPE
                if isinstance(data, str):
                    return {}

                if not isinstance(data, dict):
                    return {}

                return data

        except json.JSONDecodeError:
            return {}


def update_state(new_state):
    with lock:
        _ensure_file()
        with open(STATE_FILE, "w") as f:
            json.dump(new_state, f, indent=2)
