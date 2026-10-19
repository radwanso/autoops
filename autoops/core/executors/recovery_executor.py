import os
import subprocess


def execute_recovery(payload):

    state = payload.get("state", {})
    decision = payload.get("decision")

    service = state.get("service")

    running = state.get(
        "running",
        state.get("is_running", False)
    )

    policy = state.get(
        "policy",
        {}
    )

    response_plan = state.get(
        "response_plan",
        {}
    )

    # A healthy service with a STABLE/OBSERVE decision is not a recovery
    # attempt. Check the decision before reporting the service as already
    # running so normal monitoring logs remain accurate.
    if decision not in [
        "RECOVER",
        "RESTART"
    ]:
        return {
            "status": "SKIPPED",
            "reason": f"DECISION_NOT_EXECUTABLE:{decision}",
            "service": service
        }

    # =========================
    # ALREADY RUNNING
    # =========================

    if running:
        return {
            "status": "ALREADY_RUNNING",
            "service": service
        }

    # =========================
    # POLICY SAFETY GATE
    # =========================

    if isinstance(policy, dict):

        if policy.get("safe_mode", False):
            return {
                "status": "POLICY_BLOCKED",
                "reason": "SAFE_MODE",
                "service": service
            }

        if policy.get("allow_restart") is False:
            return {
                "status": "POLICY_BLOCKED",
                "reason": "RESTART_NOT_ALLOWED",
                "service": service
            }

    # =========================
    # RESPONSE SAFETY GATE
    # =========================

    if isinstance(response_plan, dict):

        if response_plan.get("safe_mode", False):
            return {
                "status": "RESPONSE_BLOCKED",
                "reason": "SAFE_MODE",
                "service": service
            }

        if response_plan.get("allow_restart") is False:
            return {
                "status": "RESPONSE_BLOCKED",
                "reason": "RESTART_NOT_ALLOWED",
                "service": service
            }

    # =========================
    # EXECUTION
    # =========================

    try:

        command = [
            "/bin/systemctl",
            "restart",
            service
        ]

        # AutoOps may run as an ordinary user. Use sudo in non-interactive
        # mode so a narrowly scoped sudoers rule can authorize only approved
        # service restarts without hanging for a password prompt.
        if hasattr(os, "geteuid") and os.geteuid() != 0:
            command = ["/usr/bin/sudo", "-n", *command]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30
        )

        print(
            f"[RECOVERY] "
            f"service={service} "
            f"decision={decision} "
            f"rc={result.returncode} "
            f"stderr={result.stderr}"
        )

        return {
            "status": "RESTART_SENT" if result.returncode == 0 else "FAILED",
            "service": service,
            "rc": result.returncode,
            "error": result.stderr if result.returncode != 0 else None
        }

    except Exception as e:

        return {
            "status": "FAILED",
            "service": service,
            "error": str(e)
        }
