def choose_strategy(state):

    risk = state.get(
        "risk",
        {}
    )

    behavior = state.get(
        "behavior",
        {}
    )

    cognitive = state.get(
        "cognitive_state",
        {}
    )

    reputation = state.get(
        "reputation",
        1.0
    )

    confidence = cognitive.get(
        "confidence",
        1.0
    )

    risk_level = risk.get(
        "level",
        "LOW"
    )

    # =========================
    # CRITICAL
    # =========================

    if risk_level == "CRITICAL":
        return "CONSERVATIVE"

    # =========================
    # LOW CONFIDENCE
    # =========================

    if confidence < 0.5:
        return "OBSERVE_ONLY"

    # =========================
    # UNSTABLE SERVICE
    # =========================

    if behavior.get(
        "unstable",
        False
    ):
        return "SAFE_RECOVERY"

    # =========================
    # LOW REPUTATION
    # =========================

    if reputation < 0.3:
        return "LIMITED_RECOVERY"

    # =========================
    # DEFAULT
    # =========================

    return "NORMAL"
