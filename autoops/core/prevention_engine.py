def build_preventive_actions(state_obj):

    prediction = state_obj.get(
        "prediction",
        "LOW_RISK"
    )

    reputation = state_obj.get(
        "reputation",
        "STABLE"
    )

    risk = state_obj.get(
        "risk",
        "LOW"
    )

    actions = {
        "increase_monitoring": False,
        "slow_recovery": False,
        "pre_alert": False,
        "freeze_restart": False
    }

    # =========================
    # High Prediction Risk
    # =========================

    if prediction == "HIGH_RISK":

        actions["increase_monitoring"] = True
        actions["pre_alert"] = True

    # =========================
    # Dangerous Reputation
    # =========================

    if reputation in [
        "RISKY",
        "CRITICAL"
    ]:

        actions["slow_recovery"] = True

    # =========================
    # Critical Risk
    # =========================

    if risk == "CRITICAL":

        actions["freeze_restart"] = True

    return actions
