

def opportunityDetect_liquidityGrab(data):

    analysis = data.get("analysis", {})
    rsi = analysis.get("rsi", 50)
    price = analysis.get("price", 0)
    volatility = analysis.get("volatility", 0)

    # fake "stop hunt logic"
    if rsi < 35 and volatility > 0.05:
        return {
            "type": "liquidity_grab",
            "buy": True,
            "sell": False,
            "score": 8,
            "strength": "strong",
            "entry_type": "reversal_sweep",
            "reason": "liquidity sweep downside"
        }

    if rsi > 65 and volatility > 0.05:
        return {
            "type": "liquidity_grab",
            "buy": False,
            "sell": True,
            "score": 8,
            "strength": "strong",
            "entry_type": "reversal_sweep",
            "reason": "liquidity sweep upside"
        }

    return {"type": "liquidity_grab", "buy": False, "sell": False, "score": 0}

