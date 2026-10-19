def analyze_recovery_result(
    state,
    action_result
):

    history = state.get(
        "history",
        []
    )

    recovery_policy = state.get(
        "recovery_policy",
        {}
    )

    success = action_result.get(
        "success",
        False
    )

    feedback = {
        "recovery_success": success,
        "adjust_strategy": False,
        "increase_delay": False
    }

    # =========================
    # FAILED RECOVERY
    # =========================

    if not success:

        feedback["adjust_strategy"] = True
        feedback["increase_delay"] = True

    # =========================
    # TOO MANY RESTARTS
    # =========================

    restart_count = len([
        e for e in history
        if e.get("event") == "RESTART"
    ])

    if restart_count >= 3:

        feedback["adjust_strategy"] = True

    return feedback
