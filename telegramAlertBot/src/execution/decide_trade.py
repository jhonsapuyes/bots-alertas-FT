

def decide_trade(data):

    analysis = data.get("analysis", {})
    v1 = data.get("opportunity_v1")
    v2 = data.get("opportunity_v2")

    adx = analysis.get("adx", 0)
    rsi = analysis.get("rsi", 50)
    price = analysis.get("price", 0)
    sma = analysis.get("sma", 0)
    trend = analysis.get("trend")
    momentum = data.get("momentum")

    distance_sma = (price - sma) / sma if sma else 0

    # =========================
    # MARKET TYPE
    # =========================
    if adx >= 25:
        market_type = "trend"
        chosen = v2
    elif adx <= 18:
        market_type = "range"
        chosen = v1
    else:
        return {"buy": False, "sell": False, "reason": "uncertain"}

    if not chosen:
        return {"buy": False, "sell": False, "reason": "no opportunity"}

    # =========================
    # RANGE FILTERS
    # =========================
    if market_type == "range":

        if abs(distance_sma) > 0.02:
            return {"buy": False, "sell": False, "reason": "too far from sma"}

        if chosen.get("sell") and rsi < 30:
            return {"buy": False, "sell": False, "reason": "oversold"}

        if chosen.get("buy") and rsi > 70:
            return {"buy": False, "sell": False, "reason": "overbought"}

    # =========================
    # TREND LOGIC
    # =========================
    if market_type == "trend":

        if momentum == "bearish" and not chosen.get("sell"):
            return {"buy": False, "sell": False, "reason": "momentum mismatch"}

        if momentum == "bullish" and not chosen.get("buy"):
            return {"buy": False, "sell": False, "reason": "momentum mismatch"}

        # ⚠️ RSI warning
        warning = None
        if chosen.get("sell") and rsi < 35:
            warning = "possible bounce"

        # ajustar fuerza por volumen
        if not analysis.get("volume_confirm"):
            if chosen["strength"] == "strong":
                chosen["strength"] = "medium"

    else:
        warning = None

    # =========================
    # RESULT
    # =========================
    return {
        "buy": chosen.get("buy", False),
        "sell": chosen.get("sell", False),
        "strength": chosen.get("strength"),
        "reason": chosen.get("reason"),
        "entry_type": chosen.get("entry_type"),
        "market_type": market_type,
        "rsi": rsi,
        "adx": adx,
        "distance_sma": round(distance_sma, 4),
        "warning": warning
    }
