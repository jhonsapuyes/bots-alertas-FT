

def opportunityDetect_meanReversion(data):

    analysis = data.get("analysis", {})

    price = analysis.get("price", 0)
    sma = analysis.get("sma", 0)
    rsi = analysis.get("rsi", 50)

    distance = (price - sma) / sma if sma else 0

    # condiciones de reversión
    if rsi < 30 and price < sma:
        return {
            "type": "mean_reversion",
            "buy": True,
            "sell": False,
            "score": 7,
            "strength": "medium",
            "reason": "oversold below SMA"
        }

    if rsi > 70 and price > sma:
        return {
            "type": "mean_reversion",
            "buy": False,
            "sell": True,
            "score": 7,
            "strength": "medium",
            "reason": "overbought above SMA"
        }

    return {"type": "mean_reversion", "buy": False, "sell": False, "score": 0}

