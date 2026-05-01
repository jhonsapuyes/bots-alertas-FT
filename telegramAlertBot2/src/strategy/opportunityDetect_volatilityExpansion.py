

def opportunityDetect_volatilityExpansion(data):

    analysis = data.get("analysis", {})

    volatility = analysis.get("volatility", 0)
    adx = analysis.get("adx", 0)
    rsi = analysis.get("rsi", 50)

    if volatility > 0.06 and adx > 20:

        if rsi > 55:
            return {
                "type": "volatility_expansion",
                "buy": True,
                "sell": False,
                "score": 8,
                "strength": "strong",
                "reason": "expansion bullish"
            }

        if rsi < 45:
            return {
                "type": "volatility_expansion",
                "buy": False,
                "sell": True,
                "score": 8,
                "strength": "strong",
                "reason": "expansion bearish"
            }

    return {"type": "volatility_expansion", "buy": False, "sell": False, "score": 0}

