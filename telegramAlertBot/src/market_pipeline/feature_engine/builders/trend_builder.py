

def build_trend_features(trend_data):

    if not trend_data:
        return {}

    trend_type = trend_data.get("trend", "neutral")

    # 🔹 Dirección base
    if "bullish" in trend_type:
        direction = "bullish"
        bias = "long"
    elif "bearish" in trend_type:
        direction = "bearish"
        bias = "short"
    else:
        direction = "sideways"
        bias = "neutral"

    # 🔹 Fuerza
    if "weak" in trend_type:
        strength = "weak"
    elif trend_type in ["bullish", "bearish"]:
        strength = "strong"
    else:
        strength = "neutral"

    # 🔹 Si hay tendencia real
    is_trending = direction in ["bullish", "bearish"]

    # 🔹 Métricas adicionales
    higher_highs = trend_data.get("higher_highs", 0)
    higher_lows = trend_data.get("higher_lows", 0)
    lower_highs = trend_data.get("lower_highs", 0)
    lower_lows = trend_data.get("lower_lows", 0)

    structure_score = (higher_highs + higher_lows) - (lower_highs + lower_lows)

    return {
        "trend_direction": direction,
        "trend_strength": strength,
        "is_trending": is_trending,
        "bias": bias,
        "structure_score": structure_score
    }

