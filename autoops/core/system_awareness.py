def calculate_system_state(all_services):

    critical = 0
    unstable = 0
    healthy = 0

    for service in all_services.values():

        mode = service.get(
            "mode",
            "NORMAL"
        )

        reputation = service.get(
            "reputation",
            "STABLE"
        )

        if (
            mode == "CRITICAL"
            or reputation == "CRITICAL"
        ):
            critical += 1

        elif mode in [
            "UNSTABLE",
            "DEGRADED"
        ]:
            unstable += 1

        else:
            healthy += 1

    # =========================
    # Global Awareness
    # =========================

    if critical >= 2:
        return "SYSTEM_EMERGENCY"

    if unstable >= 2:
        return "SYSTEM_UNSTABLE"

    if healthy == len(all_services):
        return "SYSTEM_HEALTHY"

    return "SYSTEM_DEGRADED"
