

def calculate_trend(candles):

    if len(candles) < 3:
        return {"trend": "neutral"}

    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]

    higher_highs = 0
    lower_highs = 0
    higher_lows = 0
    lower_lows = 0

    for i in range(1, len(candles)):

        # HIGH STRUCTURE
        if highs[i] > highs[i - 1]:
            higher_highs += 1
        else:
            lower_highs += 1

        # LOW STRUCTURE
        if lows[i] > lows[i - 1]:
            higher_lows += 1
        else:
            lower_lows += 1

    # 🔥 LÓGICA MEJORADA
    if higher_lows > lower_lows and higher_highs >= lower_highs:
        trend = "bullish"

    elif lower_highs > higher_highs and lower_lows >= higher_lows:
        trend = "bearish"

    elif higher_lows > lower_lows:
        trend = "bullish_weak"

    elif lower_highs > higher_highs:
        trend = "bearish_weak"

    else:
        trend = "sideways"

    return {
        "trend": trend,
        "higher_highs": higher_highs,
        "higher_lows": higher_lows,
        "lower_highs": lower_highs,
        "lower_lows": lower_lows
    }

