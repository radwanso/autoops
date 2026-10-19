def build_recovery_policy(state):

    strategy = state.get(
        "strategy",
        "NORMAL"
    )

    experience = state.get(
        "experience",
        {}
    )

    trust = experience.get(
        "trust",
        0.5
    )

    # =========================
    # DEFAULT POLICY
    # =========================

    policy = {
        "max_restart_attempts": 3,
        "restart_delay": 5,
        "allow_aggressive_recovery": False
    }

    # =========================
    # NORMAL
    # =========================

    if strategy == "NORMAL":

        policy["allow_aggressive_recovery"] = True
        policy["restart_delay"] = 2

    # =========================
    # LIMITED
    # =========================

    elif strategy == "LIMITED_RECOVERY":

        policy["max_restart_attempts"] = 1
        policy["restart_delay"] = 15

    # =========================
    # CONSERVATIVE
    # =========================

    elif strategy == "CONSERVATIVE":

        # A confirmed outage still gets one cautious recovery attempt. The
        # controller escalates if that actual attempt fails.
        policy["max_restart_attempts"] = 1
        policy["restart_delay"] = 30

    # =========================
    # EXPERIENCE TRUST
    # =========================

    if trust < 0.4:

        policy["max_restart_attempts"] = min(
            policy["max_restart_attempts"],
            1
        )

    return policy
