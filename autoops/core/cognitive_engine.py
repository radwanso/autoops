def build_cognitive_state(state):

    risk = state.get("risk", {})
    behavior = state.get("behavior", {})
    reputation = state.get("reputation", 1.0)
    prediction = state.get("prediction", "LOW_RISK")
    incident = state.get("incident", {})

    reasons = []

    if risk.get("level") == "HIGH":
        reasons.append(
            "high risk detected"
        )

    if behavior.get("unstable"):
        reasons.append(
            "service unstable"
        )

    if reputation < 0.4:
        reasons.append(
            "low reputation"
        )

    if prediction == "HIGH_RISK":
        reasons.append(
            "future failure predicted"
        )

    confidence = 1.0

    if len(reasons) >= 3:
        confidence = 0.9

    elif len(reasons) == 2:
        confidence = 0.7

    elif len(reasons) == 1:
        confidence = 0.6

    else:
        confidence = 0.8

    return {
        "situation": incident.get(
            "type",
            "UNKNOWN"
        ),
        "confidence": confidence,
        "reasons": reasons,
        "recommended_action": state.get(
            "decision",
            "NONE"
        )
    }
