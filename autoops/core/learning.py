def learn_from_behavior(profile, history):

    adapted = profile.copy()

    restart_events = len([
        e for e in history
        if e["event"] == "RESTART"
    ])

    success_events = len([
        e for e in history
        if e["event"] == "SUCCESS"
    ])

    fail_events = len([
        e for e in history
        if e["event"] == "FAIL"
    ])

    # =========================
    # Success Rate
    # =========================

    success_rate = (
        success_events / restart_events
        if restart_events > 0 else 1
    )

    # =========================
    # Adaptive Thresholds
    # =========================

    if success_rate < 0.4:
        adapted["restart_threshold"] = 4
        adapted["cooldown"] = 60

    elif success_rate > 0.8:
        adapted["restart_threshold"] = 2
        adapted["cooldown"] = 15

    # =========================
    # Too Many Failures
    # =========================

    if fail_events >= 5:
        adapted["escalation_threshold"] = 3

    return adapted
