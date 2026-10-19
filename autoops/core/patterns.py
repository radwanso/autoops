def detect_patterns(history):

    patterns = []

    restart_events = [
        e for e in history
        if e["event"] == "RESTART"
    ]

    fail_events = [
        e for e in history
        if e["event"] == "FAIL"
    ]

    # =========================
    # Frequent Restart Pattern
    # =========================

    if len(restart_events) >= 3:
        patterns.append({
            "type": "FREQUENT_RESTARTS",
            "severity": "HIGH"
        })

    # =========================
    # Failure Burst
    # =========================

    if len(fail_events) >= 5:
        patterns.append({
            "type": "FAILURE_BURST",
            "severity": "CRITICAL"
        })

    # =========================
    # Flapping Pattern
    # =========================

    if (
        len(restart_events) >= 2 and
        len(fail_events) >= 2
    ):
        patterns.append({
            "type": "FLAPPING_PATTERN",
            "severity": "HIGH"
        })

    return patterns
