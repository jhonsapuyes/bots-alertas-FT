

def opportunityDetect_momentumIgnition(data):

    analysis = data.get("analysis", {})

    macd = analysis.get("macd", 0)
    signal = analysis.get("signal_line", 0)
    rsi = analysis.get("rsi", 50)
    adx = analysis.get("adx", 0)

    macd_hist = macd - signal

    if adx > 25 and macd_hist > 0 and rsi > 55:
        return {
            "type": "momentum_ignition",
            "buy": True,
            "sell": False,
            "score": 9,
            "strength": "strong",
            "entry_type": "breakout_start",
            "reason": "bull momentum ignition"
        }

    if adx > 25 and macd_hist < 0 and rsi < 45:
        return {
            "type": "momentum_ignition",
            "buy": False,
            "sell": True,
            "score": 9,
            "strength": "strong",
            "entry_type": "breakdown_start",
            "reason": "bear momentum ignition"
        }

    return {"type": "momentum_ignition", "buy": False, "sell": False, "score": 0}

