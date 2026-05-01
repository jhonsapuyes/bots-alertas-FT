

import statistics

def calculate_volatility(candles, returns):

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

