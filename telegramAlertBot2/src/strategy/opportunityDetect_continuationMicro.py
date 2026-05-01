

def opportunityDetect_continuationMicro(data):

    analysis = data.get("analysis", {})

    trend = analysis.get("trend")
    rsi = analysis.get("rsi", 50)
    adx = analysis.get("adx", 0)

    if adx > 22:

        if trend == "bullish" and 50 < rsi < 70:
            return {
                "type": "continuation_micro",
                "buy": True,
                "sell": False,
                "score": 7,
                "strength": "medium",
                "entry_type": "pullback_continuation",
                "reason": "bull continuation micro"
            }

        if trend == "bearish" and 30 < rsi < 50:
            return {
                "type": "continuation_micro",
                "buy": False,
                "sell": True,
                "score": 7,
                "strength": "medium",
                "entry_type": "pullback_continuation",
                "reason": "bear continuation micro"
            }

    return {"type": "continuation_micro", "buy": False, "sell": False, "score": 0}

