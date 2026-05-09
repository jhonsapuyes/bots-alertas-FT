

def detect_exhaustion(context):
    mom = context["features"].get("momentum", {})

    if mom.get("momentum_strength") == "strong" and mom.get("continuation") is False:
        return {
            "type": "exhaustion",
            "detected": True,
            "score": 0.6,
            "side": None,
            "reason": "Momentum exhaustion detected"
        }

    return None  
