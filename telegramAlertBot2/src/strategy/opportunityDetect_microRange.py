

def opportunityDetect_microRange(data):

    analysis = data.get("analysis", {})

    adx = analysis.get("adx", 0)
    rsi = analysis.get("rsi", 50)

    if adx < 18:

        if rsi < 40:
            return {
                "type": "micro_range",
                "buy": True,
                "sell": False,
                "score": 6,
                "strength": "medium",
                "reason": "range bottom"
            }

        if rsi > 60:
            return {
                "type": "micro_range",
                "buy": False,
                "sell": True,
                "score": 6,
                "strength": "medium",
                "reason": "range top"
            }

    return {"type": "micro_range", "buy": False, "sell": False, "score": 0}

