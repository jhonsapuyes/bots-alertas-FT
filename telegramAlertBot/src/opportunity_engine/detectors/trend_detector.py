



def detect_trend(context):
    trend = context["features"].get("trend", {})

    if not trend.get("is_trending"):
        return None

    return {
        "type": "trend",
        "detected": True,
        "score": 0.75,
        "side": trend.get("bias"),
        "reason": f"Trend {trend.get('trend_direction')}"
    }

