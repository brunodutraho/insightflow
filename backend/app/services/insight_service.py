def generate_insights(current: dict, previous: dict | None = None):
    insights = []

    # fallback (caso não tenha comparação ainda)
    if not previous:
        if current["ctr"] < 0.02:
            insights.append("⚠️ Low CTR — improve creatives")
        if current["cpc"] > 2:
            insights.append("💸 High CPC — optimize targeting")
        if current["cpm"] > 50:
            insights.append("📈 High CPM — audience may be expensive")

        if not insights:
            insights.append("✅ Campaign performing well")

        return insights

    # comparação de períodos

    # CTR
    if previous["ctr"] > 0:
        change = ((current["ctr"] - previous["ctr"]) / previous["ctr"]) * 100

        if change < -10:
            insights.append(f"⚠️ CTR caiu {round(abs(change),2)}% — campanhas podem estar menos atrativas")
        elif change > 10:
            insights.append(f"🚀 CTR aumentou {round(change,2)}% — bom desempenho criativo")

    # CPC
    if previous["cpc"] > 0:
        change = ((current["cpc"] - previous["cpc"]) / previous["cpc"]) * 100

        if change > 10:
            insights.append(f"💸 CPC subiu {round(change,2)}% — custo de aquisição piorou")
        elif change < -10:
            insights.append(f"🔥 CPC caiu {round(abs(change),2)}% — mais eficiência")

    # CPM
    if previous["cpm"] > 0:
        change = ((current["cpm"] - previous["cpm"]) / previous["cpm"]) * 100

        if change > 10:
            insights.append(f"📈 CPM subiu {round(change,2)}% — tráfego mais caro")

    return insights