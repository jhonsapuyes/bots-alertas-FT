

def generate_decision(score: dict, scenario: str) -> dict:
    """
    Genera decisión final del sistema.
    """

    final_score = score["final_score"]

    # 🟢 BUY LOGIC
    if scenario in ["strong_bullish"] and final_score > 2:
        return {
            "action": "BUY",
            "confidence": min(0.9, 0.5 + final_score * 0.1)
        }

    # 🔴 SELL LOGIC
    if scenario in ["strong_bearish"] and final_score < -2:
        return {
            "action": "SELL",
            "confidence": min(0.9, 0.5 + abs(final_score) * 0.1)
        }

    # 🟡 WAIT LOGIC
    return {
        "action": "WAIT",
        "confidence": 0.6
    }

