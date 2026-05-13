

def adaptive_context(features, regime, signal):

    trend = features["trend"]
    momentum = features["momentum"]

    bullish_context = (
        trend["trend_direction"] == "bullish"
        and trend["structure_state"] in [
            "bullish",
            "bullish_recovery"
        ]
    )

    momentum_ok = (
        momentum["momentum_strength"] in [
            "moderate",
            "strong"
        ]
    )

    if bullish_context and momentum_ok:

        return {
            "allow_anticipation": True,
            "strategy_mode": "early_trend_follow",
            "risk_modifier": 0.5
        }

    return {
        "allow_anticipation": False
    }

