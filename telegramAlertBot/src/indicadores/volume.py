

import statistics


def calculate_obv(candles):

    if not candles or len(candles) < 10:
        return None

    obv = [0]

    for i in range(1, len(candles)):
        c = candles[i]["close"]
        p = candles[i - 1]["close"]
        v = candles[i]["volume"]

        if c > p:
            obv.append(obv[-1] + v)
        elif c < p:
            obv.append(obv[-1] - v)
        else:
            obv.append(obv[-1])

    return obv


def analyze_obv(obv):

    if not obv or len(obv) < 10:
        return None

    window = 5
    sample = obv[-20:]

    vol = statistics.stdev(sample) if len(sample) > 1 else 1e-9
    vol = max(vol, 1e-9)

    roc = (obv[-1] - obv[-window]) / vol

    if abs(roc) < 0.5:
        return None  # 👈 ruido

    return {
        "indicator": "OBV",
        "signal": "bullish" if roc > 0 else "bearish",
        "strength": min(abs(roc) / 10, 1.0)
    }

