

def detect_range(context):
    vol = context["features"].get("volatility", {})

    if vol.get("volatility_level") == "low":
        return {
            "type": "range",
            "detected": True,
            "score": 0.8,
            "side": None,
            "reason": "Market in range"
        }

    return None

