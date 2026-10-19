def evaluate_policy(state):

    risk = state.get("risk", {})
    behavior = state.get("behavior", {})

    risk_level = risk.get("level", "LOW")

    unstable = behavior.get(
        "unstable",
        False
    )

    safe_to_restart = behavior.get(
        "safe_to_restart",
        True
    )

    recovery_policy = state.get("recovery_policy", {})
    if not isinstance(recovery_policy, dict):
        recovery_policy = {}
    max_attempts = recovery_policy.get("max_restart_attempts", 3)
    restart_attempts = state.get("restart_attempts", 0)
    attempts_available = restart_attempts < max_attempts

    policy = {
        "safe_mode": False,
        "allow_restart": True
    }

    # A service being DOWN is classified as CRITICAL by risk_engine. Permit
    # its configured recovery when behavior analysis says a restart is safe.
    # Other critical conditions remain escalation-only.
    if risk_level == "CRITICAL":
        recoverable_outage = (
            state.get("status") == "DOWN"
            and safe_to_restart
            and attempts_available
        )
        policy["safe_mode"] = not recoverable_outage
        policy["allow_restart"] = recoverable_outage

    if not safe_to_restart or not attempts_available:
        policy["allow_restart"] = False

    elif unstable:
        policy["allow_restart"] = True

    return policy
