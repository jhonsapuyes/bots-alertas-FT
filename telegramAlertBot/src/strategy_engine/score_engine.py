

def calculate_score(features: dict) -> dict:
    """
    Convierte features en score global del mercado.
    """

    trend = features["trend"]
    momentum = features["momentum"]
    volatility = features["volatility"]

    # --- TREND SCORE ---
    trend_score = 0

    if trend["trend_direction"] == "bullish":
        trend_score += 2
    elif trend["trend_direction"] == "bearish":
        trend_score -= 2

    if trend["trend_strength"] == "strong":
        trend_score += 1
    elif trend["trend_strength"] == "weak":
        trend_score -= 0.5

    # --- MOMENTUM SCORE ---
    momentum_score = 0

    if momentum["momentum_state"] == "oversold":
        momentum_score += 2
    elif momentum["momentum_state"] == "overbought":
        momentum_score -= 2

    if momentum["momentum_strength"] == "strong":
        momentum_score += 1

    # --- VOLATILITY SCORE ---
    volatility_score = 0

    if volatility["volatility_level"] == "high":
        volatility_score -= 1
    elif volatility["volatility_level"] == "low":
        volatility_score += 0.5

    # --- FINAL SCORE ---
    final_score = trend_score + momentum_score + volatility_score

    return {
        "trend_score": trend_score,
        "momentum_score": momentum_score,
        "volatility_score": volatility_score,
        "final_score": final_score
    }

