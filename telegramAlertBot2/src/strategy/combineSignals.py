

def combine_signals(signals):

    WEIGHTS = {
        "MACD": 1.5,
        "ADX": 1.3,
        "RSI": 1.2,
        "SMA": 1.0,
        "OBV": 0.7,
        "Bollinger": 1.0
    }

    score = 0.0
    total_weight = 0

    macd_bull = macd_bear = False
    sma_bull = sma_bear = False
    adx_trend = "neutral"
    strong_trend = False
    volume_confirm = False

    for s in signals:

        signal = s.get("signal")
        strength = s.get("strength", 0)
        indicator = s.get("indicator")

        weight = WEIGHTS.get(indicator, 1)
        total_weight += weight

        if signal == "bullish":
            score += strength * weight

        elif signal == "bearish":
            score -= strength * weight

        # flags
        if indicator == "MACD":
            macd_bull = signal == "bullish"
            macd_bear = signal == "bearish"

        if indicator == "SMA":
            sma_bull = signal == "bullish"
            sma_bear = signal == "bearish"

        if indicator == "ADX":
            adx_trend = signal
            strong_trend = strength >= 0.7

        if indicator == "OBV":
            if signal == "bullish" and strength > 0.2:
                volume_confirm = True

    # 🔥 normalización (clave para estabilidad)
    normalized_score = score / max(total_weight, 1)

    return {
        "score": round(normalized_score, 2),
        "confidence": min(abs(normalized_score), 1),

        "macd_bull": macd_bull,
        "macd_bear": macd_bear,

        "sma_bull": sma_bull,
        "sma_bear": sma_bear,

        "adx_trend": adx_trend,
        "strong_trend": strong_trend,

        "volume_confirm": volume_confirm
    }

