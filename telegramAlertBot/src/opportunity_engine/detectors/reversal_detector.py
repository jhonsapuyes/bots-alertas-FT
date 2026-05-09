

def detect_reversal(context):
    features = context["features"]

    trend = features.get("trend", {})
    mom = features.get("momentum", {})

    if trend.get("trend_direction") == "bullish" and mom.get("momentum_state") == "bearish":
        return {
            "type": "reversal",
            "detected": True,
            "score": 0.8,
            "side": "short",
            "reason": "Trend-momentum divergence reversal"
        }

    return None

