def calculate_mode(state):

    fail_count = state.get("fail_count", 0)
    restart_attempts = state.get("restart_attempts", 0)
    success_count = state.get("success_count", 0)

    success_rate = (
        success_count / restart_attempts
        if restart_attempts > 0 else 1
    )

    # ====================================
    # CRITICAL
    # ====================================

    if restart_attempts >= 5:
        return "CRITICAL"

    if restart_attempts >= 3 and success_rate < 0.4:
        return "CRITICAL"

    # ====================================
    # UNSTABLE
    # ====================================

    if fail_count >= 3:
        return "UNSTABLE"

    # ====================================
    # RECOVERING
    # ====================================

    if success_count > 0 and fail_count == 0:
        return "RECOVERING"

    # ====================================
    # NORMAL
    # ====================================

    return "NORMAL"
