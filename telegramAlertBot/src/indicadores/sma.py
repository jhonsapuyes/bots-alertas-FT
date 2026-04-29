

def calculate_sma(prices, period=14):

    if len(prices) < period:
        return None

    return sum(prices[-period:]) / period


def analyze_sma(price, sma):

    if price is None or sma is None:
        return None

    diff = (price - sma) / sma

    if abs(diff) < 0.002:
        return None  # 👈 elimina ruido

    strength = min(abs(diff) * 10, 1.0)

    return {
        "indicator": "SMA",
        "signal": "bullish" if diff > 0 else "bearish",
        "strength": strength
    }
 
    