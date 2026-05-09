

def detect_momentum_ignition(context):
    mom = context["features"].get("momentum", {})

    state = mom.get("momentum_state")

    if state in ["bullish", "bearish"]:
        return {
            "type": "momentum_ignition",
            "detected": True,
            "score": 0.78,
            "side": "long" if state == "bullish" else "short",
            "reason": "Momentum ignition detected"
        }

    return None
