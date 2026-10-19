def calculate_risk(state):

    if not state:
        return {"level": "LOW", "fail_count": 0}

    if state.get("status") == "DOWN":
        return {
            "level": "CRITICAL",
            "fail_count": state.get("fail_count", 0)
        }

    behavior = state.get("behavior", {})
    events = state.get("event_analysis", {})
    fail_count = state.get("fail_count", 0)

    level = "LOW"

    if fail_count >= 5:
        level = "HIGH"

    if behavior.get("unstable") and fail_count >= 2:
        level = "HIGH"

    if events.get("error_rate", 0) > 0.7:
        level = "CRITICAL"

    return {
        "level": level,
        "fail_count": fail_count
    }
