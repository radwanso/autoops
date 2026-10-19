def classify_incident(state_obj):

    fail_count = state_obj.get("fail_count", 0)
    attempts = state_obj.get("restart_attempts", 0)
    success = state_obj.get("success_count", 0)

    mode = state_obj.get("mode", "NORMAL")

    success_rate = (
        success / attempts
        if attempts > 0 else 1
    )

    # =========================
    # Stable
    # =========================

    if fail_count == 0:
        return {
            "type": "STABLE",
            "severity": "LOW",
            "confidence": 1.0
        }

    # =========================
    # Temporary Failure
    # =========================

    if fail_count == 1:
        return {
            "type": "TRANSIENT_FAILURE",
            "severity": "LOW",
            "confidence": 0.70
        }

    # =========================
    # Flapping Service
    # =========================

    if attempts >= 3 and success_rate < 0.5:
        return {
            "type": "FLAPPING",
            "severity": "HIGH",
            "confidence": 0.85
        }

    # =========================
    # Recovery Loop
    # =========================

    if attempts >= 5:
        return {
            "type": "RECOVERY_LOOP",
            "severity": "CRITICAL",
            "confidence": 0.95
        }

    # =========================
    # Critical Mode
    # =========================

    if mode == "CRITICAL":
        return {
            "type": "CRITICAL_OUTAGE",
            "severity": "CRITICAL",
            "confidence": 0.90
        }

    # =========================
    # Generic Failure
    # =========================

    return {
        "type": "SERVICE_FAILURE",
        "severity": "MEDIUM",
        "confidence": 0.60
    }
