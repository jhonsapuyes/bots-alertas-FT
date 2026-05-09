

def detect_mean_reversion(context):
    mom = context["features"].get("momentum", {})

    rsi = mom.get("rsi", 50)

    if rsi > 70:
        return {
            "type": "mean_reversion",
            "detected": True,
            "score": 0.75,
            "side": "short",
            "reason": "Overbought mean reversion"
        }

    if rsi < 30:
        return {
            "type": "mean_reversion",
            "detected": True,
            "score": 0.75,
            "side": "long",
            "reason": "Oversold mean reversion"
        }

    return None
