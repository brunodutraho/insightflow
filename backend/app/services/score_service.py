def calculate_score(kpi: dict):
    ctr = kpi.get("ctr", 0)
    cpc = kpi.get("cpc", 0)
    cpm = kpi.get("cpm", 0)

    # normalização (valores de referência)
    ctr_score = min(ctr * 1000, 100)        # CTR bom ~ 0.05 (5%)
    cpc_score = max(100 - (cpc * 10), 0)    # menor CPC = melhor
    cpm_score = max(100 - (cpm / 2), 0)     # menor CPM = melhor

    final_score = (
        ctr_score * 0.4 +
        cpc_score * 0.3 +
        cpm_score * 0.3
    )

    final_score = int(round(final_score))

    # classificação
    if final_score >= 80:
        level = "excellent"
    elif final_score >= 60:
        level = "good"
    elif final_score >= 40:
        level = "average"
    else:
        level = "poor"

    # insights inteligentes
    insights = []

    if ctr > 0.03:
        insights.append("Strong engagement (CTR is high)")
    else:
        insights.append("CTR could be improved")

    if cpc > 2:
        insights.append("High cost per click")
    else:
        insights.append("CPC is under control")

    if cpm > 50:
        insights.append("High cost per impressions")
    else:
        insights.append("CPM is efficient")

    return {
        "score": final_score,
        "level": level,
        "details": {
            "ctr_score": round(ctr_score, 2),
            "cpc_score": round(cpc_score, 2),
            "cpm_score": round(cpm_score, 2),
        },
        "insights": insights
    }