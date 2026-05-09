

def detect_pullback(context):
    features = context["features"]

    trend = features.get("trend", {})
    momentum = features.get("momentum", {})

    if trend.get("is_trending") and momentum.get("entry_timing") in ["good_for_long", "good_for_short"]:
        return {
            "type": "pullback",
            "detected": True,
            "score": 0.7,
            "side": trend.get("bias"),
            "reason": "Pullback in trend"
        }

    return None

