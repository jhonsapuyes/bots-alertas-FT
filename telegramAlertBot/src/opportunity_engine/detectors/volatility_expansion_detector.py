

def detect_volatility_expansion(context):
    vol = context["features"].get("volatility", {})

    if vol.get("volatility_level") == "high":
        return {
            "type": "volatility_expansion",
            "detected": True,
            "score": 0.7,
            "side": None,
            "reason": "Volatility expansion"
        }

    return None

