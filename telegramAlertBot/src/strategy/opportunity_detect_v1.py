

def opportunity_detect_v1(ctx):

    d = ctx.get("data", {})

    adx = d.get("adx")
    price = d.get("price")
    sma = d.get("sma")
    macd = d.get("macd")
    signal = d.get("signal")
    bandwidth = d.get("volatility")

    if None in (adx, price, sma, macd, signal, bandwidth):
        return None

    range_score = 0

    if adx < 20:
        range_score += 2

    if abs(price - sma) / sma < 0.01:
        range_score += 2

    if abs(macd - signal) / max(price, 1e-9) < 0.001:
        range_score += 1

    if bandwidth < 0.03:
        range_score += 1

    if range_score < 3:
        return None

    # 🎯 lógica más precisa
    if price < sma:
        action = "buy"
    else:
        action = "sell"

    return {
        "buy": action == "buy",
        "sell": action == "sell",
        "strength": "medium",
        "reason": "range mean reversion",
        "score": range_score
    }

