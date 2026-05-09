

def detect_continuation_micro(context):
    features = context["features"]

    trend = features.get("trend", {})
    vol = features.get("volatility", {})

    if trend.get("is_trending") and vol.get("volatility_level") == "low":
        return {
            "type": "continuation_micro",
            "detected": True,
            "score": 0.7,
            "side": trend.get("bias"),
            "reason": "Micro continuation in trend"
        }

    return None
