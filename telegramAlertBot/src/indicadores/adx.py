

import statistics


def calculate_adx(candles, period=14):

    if not candles or len(candles) < period + 25:
        return None, None

    tr, plus_dm, minus_dm = [], [], []

    for i in range(1, len(candles)):
        h = candles[i]["high"]
        l = candles[i]["low"]
        cp = candles[i - 1]["close"]

        tr.append(max(h - l, abs(h - cp), abs(l - cp)))

        up = h - candles[i - 1]["high"]
        down = candles[i - 1]["low"] - l

        plus_dm.append(up if up > down and up > 0 else 0)
        minus_dm.append(down if down > up and down > 0 else 0)

    def wilder(values, p):
        s = sum(values[:p])
        result = []

        for i in range(p, len(values)):
            s = (s * (p - 1) + values[i]) / p
            result.append(s)

        return result

    tr_s = wilder(tr, period)
    plus_s = wilder(plus_dm, period)
    minus_s = wilder(minus_dm, period)

    size = min(len(tr_s), len(plus_s), len(minus_s))

    dx = []

    for i in range(size):
        if tr_s[i] <= 1e-12:
            dx.append(0)
            continue

        pdi = (plus_s[i] / tr_s[i]) * 100
        mdi = (minus_s[i] / tr_s[i]) * 100

        denom = pdi + mdi
        if denom <= 1e-12:
            dx.append(0)
            continue

        dx.append(abs(pdi - mdi) / denom * 100)

    if len(dx) < period:
        return None, None

    adx = sum(dx[-period:]) / period

    plus_avg = statistics.mean(plus_s[-10:])
    minus_avg = statistics.mean(minus_s[-10:])

    trend = "bullish" if plus_avg > minus_avg else "bearish"

    return adx, trend


def analyze_adx(adx, trend):

    if adx is None or adx < 20:
        return None  # 👈 filtro, no señal

    strength = 0.5
    if adx > 40:
        strength = 1.0
    elif adx > 30:
        strength = 0.8

    return {
        "indicator": "ADX",
        "signal": trend,
        "strength": strength
    }

