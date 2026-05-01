

def opportunityDetect_breakout(ctx):

    d = ctx.get("data", {})

    adx = d.get("adx")
    price = d.get("price")
    sma = d.get("sma")
    volatility = d.get("volatility")
    macd = d.get("macd")
    signal = d.get("signal")

    if None in (adx, price, sma, volatility, macd, signal):
        return None

    breakout_score = 0

    # 🧠 compresión previa
    if volatility < 0.03:
        breakout_score += 2

    # 🧠 expansión
    if volatility > 0.05:
        breakout_score += 2

    # 🧠 ADX creciendo (inicio de tendencia)
    if adx > 22:
        breakout_score += 1

    macd_diff = macd - signal

    if macd_diff > 0:
        direction = "bullish"
        breakout_score += 1
    elif macd_diff < 0:
        direction = "bearish"
        breakout_score += 1
    else:
        return None

    if breakout_score < 4:
        return None

    return {
        "buy": direction == "bullish",
        "sell": direction == "bearish",
        "strength": "strong",
        "reason": "volatility breakout",
        "score": breakout_score
    }

