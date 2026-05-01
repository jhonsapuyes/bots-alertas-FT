

def opportunityDetect_pullback(ctx):

    d = ctx.get("data", {})
    analysis = ctx.get("analysis", {})

    adx = d.get("adx")
    rsi = d.get("rsi")
    price = d.get("price")
    sma = d.get("sma")
    macd = d.get("macd")
    signal = d.get("signal")

    trend = analysis.get("trend")

    if None in (adx, rsi, price, sma, macd, signal, trend):
        return None

    pullback_score = 0

    # 🧠 tendencia fuerte
    if adx > 25:
        pullback_score += 2

    macd_diff = macd - signal

    # 🔻 pullback en tendencia bajista
    if trend == "bearish":
        if 35 < rsi < 50:
            pullback_score += 2
        if macd_diff > -5:
            pullback_score += 1

        direction = "bearish"

    # 🔺 pullback en tendencia alcista
    elif trend == "bullish":
        if 50 < rsi < 65:
            pullback_score += 2
        if macd_diff < 5:
            pullback_score += 1

        direction = "bullish"

    else:
        return None

    # 🧠 cercanía a la media
    distance = abs(price - sma) / sma
    if distance < 0.02:
        pullback_score += 1

    if pullback_score < 4:
        return None

    return {
        "buy": direction == "bullish",
        "sell": direction == "bearish",
        "strength": "medium",
        "reason": "trend pullback",
        "entry_type": "reentry",
        "score": pullback_score
    }

