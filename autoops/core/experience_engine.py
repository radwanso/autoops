def evaluate_experience(memory_entry):

    failures = memory_entry.get(
        "total_failures",
        0
    )

    recoveries = memory_entry.get(
        "total_recoveries",
        0
    )

    restarts = memory_entry.get(
        "total_restarts",
        0
    )

    # =========================
    # EXPERIENCE SCORE
    # =========================

    score = (
        recoveries
        - failures
        - (restarts * 0.5)
    )

    # =========================
    # EXPERIENCE LEVEL
    # =========================

    if score >= 10:
        return {
            "level": "EXPERIENCED",
            "trust": 0.9
        }

    if score >= 0:
        return {
            "level": "LEARNING",
            "trust": 0.6
        }

    return {
        "level": "UNSTABLE",
        "trust": 0.3
    }
