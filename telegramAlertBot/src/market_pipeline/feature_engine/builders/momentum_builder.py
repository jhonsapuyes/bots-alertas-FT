

def build_momentum_features(momentum_data):

    if not momentum_data:
        return {}

    state = momentum_data.get("momentum", "neutral")
    rsi = momentum_data.get("rsi", 50)
    momentum_value = momentum_data.get("momentum_value", 0)

    # 🔹 Fuerza del momentum
    if abs(momentum_value) > 10:
        strength = "strong"
    elif abs(momentum_value) > 3:
        strength = "moderate"
    else:
        strength = "weak"

    # 🔹 Timing de entrada
    if state == "overbought":
        entry_timing = "bad_for_long"
    elif state == "oversold":
        entry_timing = "bad_for_short"
    elif state == "bullish":
        entry_timing = "good_for_long"
    elif state == "bearish":
        entry_timing = "good_for_short"
    else:
        entry_timing = "neutral"

    # 🔹 Continuación del movimiento
    if state in ["bullish", "bearish"] and strength == "strong":
        continuation = True
    else:
        continuation = False

    return {
        "momentum_state": state,
        "momentum_strength": strength,
        "entry_timing": entry_timing,
        "continuation": continuation,
        "rsi": rsi
    }

