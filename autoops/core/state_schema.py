def normalize_state(state: dict, service_name: str = "unknown") -> dict:
    """
    Normalize runtime state into the canonical AutoOps state shape.

    This is the single source of truth for required state keys.
    """

    if not isinstance(state, dict):
        state = {}

    normalized = dict(state)

    defaults = {
        "service": service_name,
        "status": "UP",
        "running": False,

        "fail_count": 0,
        "restart_attempts": 0,
        "success_count": 0,

        "history": [],
        "last_failure_time": 0,
        "last_fix_time": 0,

        "mode": "NORMAL",
        "profile": {},

        "metrics": {},
        "behavior": {},
        "incident": {},
        "event_analysis": {},

        "prediction": {},
        "risk": {"level": "LOW"},

        "strategy": "NORMAL",
        "decision": "OBSERVE",

        "recovery_policy": {},
        "policy": {},
        "intent": "UNKNOWN",
        "response_plan": {},

        "reputation": 1.0,
        "experience": {},

        "cognitive_state": {},
    }

    for key, default in defaults.items():
        normalized.setdefault(key, default)

    return normalized
