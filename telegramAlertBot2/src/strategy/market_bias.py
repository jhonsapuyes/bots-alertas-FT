

def market_bias(data):

    price = data.get("price")
    sma = data.get("sma")
    macd = data.get("macd")
    signal = data.get("signal")
    rsi = data.get("rsi")
    adx = data.get("adx")
    trend = data.get("trend")

    if None in (price, sma, macd, signal, rsi, adx):
        return {}

    macd_hist = macd - signal
    distance = (price - sma) / sma

    # =========================
    # 🧠 CORTO PLAZO
    # =========================
    if macd_hist > 0 and rsi > 50:
        short_term = "bullish"
    elif macd_hist < 0 and rsi < 50:
        short_term = "bearish"
    else:
        short_term = "neutral"

    # =========================
    # 📊 MEDIANO PLAZO
    # =========================
    if price > sma and trend == "bullish":
        mid_term = "bullish"
    elif price < sma and trend == "bearish":
        mid_term = "bearish"
    else:
        mid_term = "neutral"

    # =========================
    # 🏛️ LARGO PLAZO
    # =========================
    if adx > 25:
        long_term = trend
    else:
        long_term = "range"

    # =========================
    # 🎯 CONFIANZA
    # =========================
    alignment = sum([
        short_term == mid_term,
        mid_term == long_term
    ])

    if alignment == 2:
        confidence = "high"
    elif alignment == 1:
        confidence = "medium"
    else:
        confidence = "low"

    # =========================
    # 🔮 ESCENARIO (NUEVO)
    # =========================
    if short_term != mid_term and mid_term == long_term:
        scenario = "pullback"

    elif short_term != mid_term and mid_term != long_term:
        scenario = "possible_reversal"

    else:
        scenario = "trend_continuation"

    return {
        "short_term": short_term,
        "mid_term": mid_term,
        "long_term": long_term,
        "confidence": confidence,
        "scenario": scenario,  # 👈 añadido sin romper nada
        "distance_sma": round(distance, 4)
    }

