

def opportunity_detect_v21(ctx):

    d = ctx.get("data", {})
    analysis = ctx.get("analysis", {})

    adx = d.get("adx")
    macd = d.get("macd")
    signal = d.get("signal")
    price = d.get("price")
    sma = d.get("sma")
    trend = d.get("trend")

    volume_confirm = analysis.get("volume_confirm")

    if None in (adx, macd, signal, price, sma):
        return None

    impulse_score = 0

    if adx > 25:
        impulse_score += 2

    if macd > signal:
        impulse_score += 2

    if abs(price - sma) / sma > 0.02:
        impulse_score += 1

    if impulse_score < 3:
        return None

    # 🔥 calidad de entrada
    distance = abs(price - sma) / sma

    if distance < 0.01:
        entry_type = "pullback"
    elif distance < 0.03:
        entry_type = "continuation"
    else:
        entry_type = "overextended"

    return {
        "buy": trend == "bullish",
        "sell": trend == "bearish",
        "strength": "strong" if volume_confirm else "medium",
        "reason": "trend continuation",
        "entry_type": entry_type,
        "score": impulse_score
    }


def opportunity_detect_v2(ctx):

    d = ctx.get("data", {})
    analysis = ctx.get("analysis", {})

    adx = d.get("adx")
    macd = d.get("macd")
    signal = d.get("signal")
    price = d.get("price")
    sma = d.get("sma")

    volume_confirm = analysis.get("volume_confirm")

    if None in (adx, macd, signal, price, sma):
        return None

    impulse_score = 0

    # 🔥 ADX (fuerza)
    if adx > 25:
        impulse_score += 2

    # 🔥 MACD DIRECCIONAL (FIX REAL)
    macd_diff = macd - signal

    if macd_diff > 0:
        impulse_score += 2
        direction = "bullish"

    elif macd_diff < 0:
        impulse_score += 2
        direction = "bearish"
    else:
        return None

    # 🔥 separación de media (estructura)
    distance = abs(price - sma) / sma
    if distance > 0.02:
        impulse_score += 1

    if impulse_score < 3:
        return None

    # 🎯 tipo de entrada
    if distance < 0.01:
        entry_type = "pullback"
    elif distance < 0.03:
        entry_type = "continuation"
    else:
        entry_type = "overextended"

    return {
        "buy": direction == "bullish",
        "sell": direction == "bearish",
        "strength": "strong" if volume_confirm else "medium",
        "reason": "trend continuation",
        "entry_type": entry_type,
        "score": impulse_score
    }

