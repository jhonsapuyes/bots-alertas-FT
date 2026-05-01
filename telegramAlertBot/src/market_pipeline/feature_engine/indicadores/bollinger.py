

import statistics

def calculate_bollinger(candles, period=20, std_dev=2):
    if not candles or len(candles) < period:
        return None, None, None, None

    closes = [c["close"] for c in candles[-period:]]

    sma = sum(closes) / period
    std = statistics.stdev(closes)

    if std < 1e-9:
        return None, sma, None, 0

    upper = sma + std_dev * std
    lower = sma - std_dev * std

    bandwidth = (upper - lower) / sma

    return upper, sma, lower, bandwidth


def analyze_bollinger(price, upper, lower):
    if price is None or upper is None or lower is None:
        return None

    if price > upper:
        return {
            "indicator": "Bollinger",
            "signal": "bearish",
            "strength": min((price - upper) / upper, 1.0)
        }

    if price < lower:
        return {
            "indicator": "Bollinger",
            "signal": "bullish",
            "strength": min((lower - price) / lower, 1.0)
        }

    return None

