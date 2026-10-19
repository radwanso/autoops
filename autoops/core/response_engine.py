def build_response_plan(state_obj):
    intent = state_obj.get(
        "intent",
        "UNKNOWN"
    )

    policy = state_obj.get(
        "policy",
        {}
    )

    risk = state_obj.get(
        "risk",
        {}
    )

    # Normalize policy
    if not isinstance(policy, dict):
        policy = {}

    # Normalize risk
    if isinstance(risk, dict):
        risk_level = risk.get("level", "LOW")
    else:
        risk_level = str(risk or "LOW")

    response = {
        "allow_restart": True,
        "send_alert": False,
        "cooldown": 30,
        "safe_mode": False,
        "escalate": False
    }

    # =========================
    # INTENT
    # =========================

    if intent == "TRANSIENT_FAILURE":
        response["allow_restart"] = True

    elif intent == "AGGRESSIVE_FAILURE":
        response["send_alert"] = True
        response["cooldown"] = 120

    elif intent == "PERSISTENT_FAILURE":
        response["safe_mode"] = True
        response["escalate"] = True
        response["allow_restart"] = False

    # =========================
    # POLICY OVERRIDE
    # =========================

    if policy.get("safe_mode", False):
        response["safe_mode"] = True

    if policy.get("allow_restart") is False:
        response["allow_restart"] = False

    # =========================
    # RISK OVERRIDE
    # =========================

    if risk_level == "CRITICAL":
        response["send_alert"] = True
        response["escalate"] = True

        # A confirmed service outage can still use the policy-approved
        # recovery path. Critical conditions without that approval stay blocked.
        recoverable_outage = (
            state_obj.get("status") == "DOWN"
            and policy.get("allow_restart") is True
            and not policy.get("safe_mode", False)
            and intent != "PERSISTENT_FAILURE"
        )
        response["safe_mode"] = not recoverable_outage
        response["allow_restart"] = recoverable_outage

    return response
