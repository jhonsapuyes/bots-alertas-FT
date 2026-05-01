

# feature_engine/builders/feature_vector.py

def build_feature_vector(trend, momentum, volatility):
    """
    Combina todas las features en una decisión final de mercado

    Args:
        trend (dict)
        momentum (dict)
        volatility (dict)

    Returns:
        dict
    """

    trend_direction = trend.get("trend_direction")
    trend_strength = trend.get("trend_strength")

    momentum_state = momentum.get("momentum_state")
    entry_timing = momentum.get("entry_timing")

    volatility_level = volatility.get("volatility_level")

    # 🔥 Lógica principal de decisión

    # 1. Mercado alcista pero sobrecomprado
    if trend_direction == "bullish" and momentum_state == "overbought":
        market_state = "bullish_exhausted"
        action = "wait"
        confidence = 0.7

    # 2. Mercado alcista con buen timing
    elif trend_direction == "bullish" and entry_timing == "good_for_long":
        market_state = "bullish_continuation"
        action = "buy"
        confidence = 0.8 if trend_strength == "strong" else 0.65

    # 3. Mercado bajista
    elif trend_direction == "bearish":
        if momentum_state == "oversold":
            market_state = "bearish_exhausted"
            action = "wait"
            confidence = 0.6
        else:
            market_state = "bearish_continuation"
            action = "sell"
            confidence = 0.75

    # 4. Lateral
    else:
        market_state = "sideways"
        action = "wait"
        confidence = 0.5

    # 5. Ajuste por volatilidad
    if volatility_level == "high":
        confidence *= 0.85  # reduce confianza en alta volatilidad

    return {
        "market_state": market_state,
        "action": action,
        "confidence": round(confidence, 2),

        # debug útil
        "context": {
            "trend": trend,
            "momentum": momentum,
            "volatility": volatility
        }
    }

