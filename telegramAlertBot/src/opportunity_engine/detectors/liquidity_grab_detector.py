

def detect_liquidity_grab(context):
    vol = context["features"].get("volatility", {})

    if vol.get("volatility_level") == "high":
        return {
            "type": "liquidity_grab",
            "detected": True,
            "score": 0.65,
            "side": None,
            "reason": "Possible liquidity sweep"
        }

    return None
