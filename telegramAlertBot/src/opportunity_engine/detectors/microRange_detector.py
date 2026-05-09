

def detect_micro_range(context):
    vol = context["features"].get("volatility", {})

    if vol.get("avg_range", 0) < 5:
        return {
            "type": "micro_range",
            "detected": True,
            "score": 0.7,
            "side": None,
            "reason": "Micro range compression"
        }

    return None  
