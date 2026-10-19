import json
import os
import tempfile

MEMORY_FILE = "autoops/data/memory.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}

    try:
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            return {}

        return data

    except (json.JSONDecodeError, OSError) as e:
        print(f"[MEMORY LOAD ERROR] {e}")
        return {}


def save_memory(memory):
    directory = os.path.dirname(MEMORY_FILE)

    os.makedirs(directory, exist_ok=True)

    fd, temp_file = tempfile.mkstemp(
        dir=directory,
        prefix=".memory-",
        suffix=".tmp"
    )

    try:
        with os.fdopen(fd, "w") as f:
            json.dump(
                memory,
                f,
                indent=2
            )
            f.flush()
            os.fsync(f.fileno())

        os.replace(temp_file, MEMORY_FILE)

    except Exception:
        try:
            os.unlink(temp_file)
        except FileNotFoundError:
            pass

        raise
