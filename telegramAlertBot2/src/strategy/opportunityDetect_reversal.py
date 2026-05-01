

def opportunityDetect_reversal(ctx):

    d = ctx.get("data", {})
    fatigue = ctx.get("fatigue", {})
    analysis = ctx.get("analysis", {})

    rsi = d.get("rsi")
    macd = d.get("macd")
    signal = d.get("signal")
    trend = analysis.get("trend")

    if None in (rsi, macd, signal, trend):
        return None

    macd_diff = macd - signal
    fatigue_phase = fatigue.get("phase")

    reversal_score = 0

    # 🧠 condición base: agotamiento
    if fatigue_phase == "exhaustion":
        reversal_score += 2

    # 🔄 divergencia básica
    if trend == "bearish" and rsi > 45 and macd_diff > 0:
        reversal_score += 2
        direction = "bullish"

    elif trend == "bullish" and rsi < 55 and macd_diff < 0:
        reversal_score += 2
        direction = "bearish"

    else:
        return None

    if reversal_score < 3:
        return None

    return {
        "buy": direction == "bullish",
        "sell": direction == "bearish",
        "strength": "weak",
        "reason": "early reversal",
        "score": reversal_score
    }

