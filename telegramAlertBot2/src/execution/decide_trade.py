

def decide_trade(ctx, decision):

    if not decision:
        return None

    if not decision.get("buy") and not decision.get("sell"):
        return None

    data = ctx.get("data", {})
    analysis = ctx.get("analysis", {})
    fatigue = ctx.get("fatigue", {})
    bias = data.get("bias", {})

    # =========================
    # 📊 DATA
    # =========================
    rsi = analysis.get("rsi", 50)
    trend = analysis.get("trend")
    price = analysis.get("price", 0)
    sma = analysis.get("sma", 0)
    volatility = analysis.get("volatility", 0)

    distance_sma = (price - sma) / sma if sma else 0

    # =========================
    # 🚫 FILTROS DUROS
    # =========================
    if decision.get("buy") and rsi > 70:
        return None

    if decision.get("sell") and rsi < 30:
        return None

    if abs(distance_sma) > 0.04:
        return None

    if volatility < 0.002:
        return None

    # =========================
    # 🧠 FATIGUE
    # =========================
    if fatigue:
        phase = fatigue.get("phase")

        if phase == "exhaustion":
            return None

    # =========================
    # ⚖️ AJUSTE DE FUERZA
    # =========================
    strength = decision.get("strength", "neutral")

    if fatigue:
        phase = fatigue.get("phase")

        if phase == "mature":
            if strength == "strong":
                strength = "medium"
            elif strength == "medium":
                strength = "weak"

        elif phase in ["trend", "accelerating"]:
            if strength == "medium":
                strength = "strong"

    # =========================
    # 🧠 TIMING SIMPLE
    # =========================
    timing = "neutral"

    if trend == "bearish":
        if 30 <= rsi <= 45:
            timing = "good_sell"
        else:
            timing = "late_sell"

    elif trend == "bullish":
        if 55 <= rsi <= 70:
            timing = "good_buy"
        else:
            timing = "late_buy"

    # =========================
    # 📦 RESULTADO
    # =========================
    result = decision.copy()

    result.update({
        "strength": strength,
        "timing": timing,
        "filtered": True
    })

    return result

