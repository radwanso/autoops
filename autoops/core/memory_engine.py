# autoops/core/memory_engine.py

def update_memory(memory, state_obj):
    if memory is None:
        memory = {}

    if state_obj is None:
        return memory

    service = (
        state_obj.get("service")
        or state_obj.get("name")
        or "unknown"
    )

    if service not in memory:
        memory[service] = {
            "incidents": [],
            "reputation_score": 1.0,
            "total_failures": 0,
            "total_restarts": 0,
            "total_recoveries": 0,
            "risk_history": [],
            "modes": []
        }

    entry = memory[service]

    # defaults safety
    entry.setdefault("incidents", [])
    entry.setdefault("reputation_score", 1.0)
    entry.setdefault("total_failures", 0)
    entry.setdefault("total_restarts", 0)
    entry.setdefault("total_recoveries", 0)
    entry.setdefault("risk_history", [])
    entry.setdefault("modes", [])

    # SAFE extraction
    fail_count = state_obj.get("fail_count", 0)
    restart_attempts = state_obj.get("restart_attempts", 0)
    success_count = state_obj.get("success_count", 0)

    if fail_count > 0:
        entry["total_failures"] += fail_count
    if restart_attempts > 0:
        entry["total_restarts"] += restart_attempts
    if success_count > 0:
        entry["total_recoveries"] += success_count

    # risk tracking
    risk = state_obj.get("risk", {"level": "LOW"})
    if not entry["risk_history"] or entry["risk_history"][-1] != risk:
        entry["risk_history"].append(risk)
    entry["risk_history"] = entry["risk_history"][-20:]

    # mode tracking
    mode = state_obj.get("mode", "NORMAL")
    if not entry["modes"] or entry["modes"][-1] != mode:
        entry["modes"].append(mode)
        entry["modes"] = entry["modes"][-20:]

    # incidents
    incident = state_obj.get("incident")
    if incident:
        entry["incidents"].append(incident)
        entry["incidents"] = entry["incidents"][-20:]

    # reputation update
    if "reputation" in state_obj:
        entry["reputation_score"] = state_obj["reputation"]

    return memory

def memory_update_handler(payload):
    memory = payload["memory"]
    state = payload["state"]
    return update_memory(memory, state)
