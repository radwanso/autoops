def evaluate_behavior(state):

    fail_count = state.get("fail_count", 0)
    profile = state.get("profile", {})

    restart_threshold = profile.get("restart_threshold", 2)
    behavior = {
        "unstable": False,
        "safe_to_restart": True
    }

    if fail_count >= restart_threshold:
        behavior["unstable"] = True

    return behavior
