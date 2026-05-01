

def calculate_ema(prices, period=14):
    if len(prices) < period:
        return None

    k = 2 / (period + 1)
    ema_values = [prices[0]]

    for price in prices[1:]:
        ema_values.append(price * k + ema_values[-1] * (1 - k))

    return ema_values[-1]


def analyze_ema(price, ema, ema_prev=None, volatility=0.01):
    if ema is None:
        return None

    threshold = max(volatility, 0.005)
    diff = (price - ema) / ema

    slope = None
    if ema_prev is not None:
        slope = ema - ema_prev

    if diff > threshold:
        return {
            "indicator": "EMA",
            "signal": "bullish",
            "strength": min(abs(diff) * 10, 1.0),
            "slope": slope
        }

    if diff < -threshold:
        return {
            "indicator": "EMA",
            "signal": "bearish",
            "strength": min(abs(diff) * 10, 1.0),
            "slope": slope
        }

    return {
        "indicator": "EMA",
        "signal": "neutral",
        "strength": 0.1,
        "slope": slope
    }

