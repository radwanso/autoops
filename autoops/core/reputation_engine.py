def calculate_reputation(memory_entry):

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

    score = 1.0

    # عقوبات
    score -= failures * 0.08
    score -= restarts * 0.03

    # مكافآت
    score += recoveries * 0.05

    # Clamp
    if score < 0:
        score = 0.0

    if score > 1:
        score = 1.0

    return round(score, 2)
