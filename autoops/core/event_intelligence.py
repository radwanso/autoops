def analyze_events(history):

    restart_count = len([
        e for e in history
        if e["event"] == "RESTART"
    ])

    fail_count = len([
        e for e in history
        if e["event"] == "FAIL"
    ])

    success_count = len([
        e for e in history
        if e["event"] == "SUCCESS"
    ])

    recovery_rate = (
        success_count / restart_count
        if restart_count > 0 else 1
    )

    unstable = fail_count >= 3

    restart_loop = restart_count >= 5

    success_actions = len([
    e for e in history
    if e["event"] == "ACTION_SUCCESS"
    ])

    action_success_rate = (
        success_actions /
        max(1, restart_count + len([
            e for e in history if "ACTION_" in e["event"]
        ]))
    )

    return {
        "restart_count": restart_count,
        "fail_count": fail_count,
        "success_count": success_count,
        "recovery_rate": round(recovery_rate, 2),
        "unstable": unstable,
        "restart_loop": restart_loop,
        "success_actions": success_actions
    }
