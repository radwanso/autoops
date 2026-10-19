def decide(state):

    behavior = state.get(
        "behavior",
        {}
    )

    risk = state.get(
        "risk",
        {}
    )

    policy = state.get(
        "policy",
        {}
    )

    cognitive = state.get(
        "cognitive_state",
        {}
    )

    fail_count = state.get(
        "fail_count",
        0
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
    # SAFE MODE
    # =========================

    if policy.get(
        "safe_mode",
        False
    ):
        return "ESCALATE"

    # A DOWN service is critical by definition in risk_engine. If the policy
    # explicitly permits recovery, do not wait for fail_count to reach two:
    # it counts DOWN transitions, so it will not rise on every engine tick.
    if (
        state.get("status") == "DOWN"
        and policy.get("allow_restart", False)
    ):
        return "RESTART"

    # =========================
    # CRITICAL
    # =========================

    if risk_level == "CRITICAL":
        return "ESCALATE"

    # =========================
    # UNSTABLE
    # =========================

    if behavior.get(
        "unstable",
        False
    ):

        if fail_count >= 2:
            return "RESTART"

        return "OBSERVE"

    # =========================
    # HEALTHY
    # =========================

    if (
        confidence >= 0.7
        and risk_level == "LOW"
    ):
        return "STABLE"

    # =========================
    # DEFAULT
    # =========================

    return "OBSERVE"
