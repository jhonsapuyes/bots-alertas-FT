

import statistics

def calculate_volatility1(candles, returns):

    # 1. desviación estándar de returns
    if len(returns) > 1:
        std_dev = statistics.stdev(returns)
    else:
        std_dev = 0

    # 2. rango promedio de velas
    ranges = []
    for c in candles:
        r = c["high"] - c["low"]
        ranges.append(r)

    avg_range = sum(ranges) / len(ranges) if ranges else 0

    return {
        "std_dev": std_dev,
        "avg_range": avg_range
    }


import statistics
from .indicadores.indicator_engine import calculate_indicators


def calculate_volatility(candles, returns, indicators=None):

    indicators = indicators or calculate_indicators(candles)

    # 🔹 desviación estándar
    if len(returns) > 1:
        std_dev = statistics.stdev(returns)
    else:
        std_dev = 0

    # 🔹 rango promedio
    ranges = [(c["high"] - c["low"]) for c in candles]
    avg_range = sum(ranges) / len(ranges) if ranges else 0

    # 🔥 bollinger (contexto real)
    bb = indicators.get("bollinger", {})
    bb_position = bb.get("position")

    if bb_position in ["above_band", "below_band"]:
        volatility_level = "high"
    else:
        volatility_level = "normal"

    return {
        "std_dev": std_dev,
        "avg_range": avg_range,
        "volatility_level": volatility_level
    }

