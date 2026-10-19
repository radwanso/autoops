def predict_failure(event_analysis, reputation):

    restart_loop = event_analysis.get(
        "restart_loop",
        False
    )

    instability = event_analysis.get(
        "instability_score",
        0
    )

    failure_ratio = event_analysis.get(
        "failure_ratio",
        0
    )

    # =========================
    # Prediction Logic
    # =========================

    if restart_loop:
        return "HIGH_RISK"

    if instability >= 7:
        return "HIGH_RISK"

    if failure_ratio >= 0.6:
        return "MEDIUM_RISK"

    if reputation in [
        "RISKY",
        "CRITICAL"
    ]:
        return "MEDIUM_RISK"

    return "LOW_RISK"
