def analyze_social(metrics):
    if not metrics:
        return None

    latest = metrics[-1]

    insights = []

    if latest.engagement_rate < 1:
        insights.append("Engagement baixo")

    if latest.engagement_rate > 5:
        insights.append("Ótimo engajamento")

    return {
        "followers": latest.followers,
        "engagement_rate": latest.engagement_rate,
        "insights": insights
    }