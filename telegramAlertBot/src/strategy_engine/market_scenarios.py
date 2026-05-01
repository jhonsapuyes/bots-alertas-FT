

def classify_market(score: dict, features: dict) -> str:
    """
    Convierte score + features en escenario de mercado.
    """

    final_score = score["final_score"]

    trend = features["trend"]
    momentum = features["momentum"]

    # 🔥 ESCENARIOS PRINCIPALES

    if final_score >= 3:
        if momentum["momentum_state"] == "overbought":
            return "bullish_exhausted"
        return "strong_bullish"

    if final_score <= -3:
        if momentum["momentum_state"] == "oversold":
            return "bearish_exhausted"
        return "strong_bearish"

    # 🔄 TRANSICIÓN / LATERAL
    if abs(final_score) <= 1:
        return "sideways_market"

    # ⚠️ BREAKOUT / RISK
    if volatility_risk(features):
        return "breakout_or_fakeout"

    return "neutral"


def volatility_risk(features):
    return features["volatility"]["volatility_level"] == "high"

