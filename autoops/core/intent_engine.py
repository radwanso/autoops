def classify_intent(state_obj):

    fail_count = state_obj.get(
        "fail_count",
        0
    )

    risk = state_obj.get(
        "risk",
        "LOW"
    )

    reputation = state_obj.get(
        "reputation",
        "STABLE"
    )

    incident = state_obj.get(
        "incident",
        {}
    )

    incident_type = incident.get(
        "type",
        "UNKNOWN"
    )

    patterns = state_obj.get(
        "patterns",
        []
    )

    # =========================
    # Recovery Loops
    # =========================

    if incident_type == "RECOVERY_LOOP":
        return "SYSTEM_INSTABILITY"

    # =========================
    # Failure Burst
    # =========================

    for pattern in patterns:

        if pattern["type"] == "FAILURE_BURST":
            return "AGGRESSIVE_FAILURE"

    # =========================
    # High Risk + Bad Reputation
    # =========================

    if (
        risk == "CRITICAL"
        and reputation in [
            "FAILING",
            "CRITICAL"
        ]
    ):
        return "PERSISTENT_FAILURE"

    # =========================
    # Simple Failure
    # =========================

    if fail_count <= 2:
        return "TRANSIENT_FAILURE"

    # =========================
    # Unknown
    # =========================

    return "UNKNOWN_BEHAVIOR"
