def adapt_profile(profile, events, risk):

    adapted = profile.copy()

    recovery_rate = events.get("recovery_rate", 1)
    restart_loop = events.get("restart_loop", False)

    risk_level = risk.get("level", "LOW")

    # إذا الإصلاحات تنجح
    if recovery_rate > 0.8:
        adapted["restart_threshold"] = max(
            1,
            profile.get("restart_threshold", 2) - 1
        )

    # إذا الإصلاحات سيئة
    if recovery_rate < 0.5:
        adapted["restart_threshold"] = (
            profile.get("restart_threshold", 2) + 1
        )

    # loop خطير
    if restart_loop:
        adapted["escalation_threshold"] = 2

    # خطر حرج
    if risk_level == "CRITICAL":
        adapted["cooldown"] = 120

    return adapted
