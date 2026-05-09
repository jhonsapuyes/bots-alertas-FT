

def detect_breakout(context):
    features = context["features"]
    vol = features.get("volatility", {})
    trend = features.get("trend", {})

    if vol.get("volatility_level") == "high" and trend.get("is_trending"):
        return {
            "type": "breakout",
            "detected": True,
            "score": 0.8,
            "side": trend.get("bias"),
            "reason": "High volatility breakout setup"
        }

    return None
    