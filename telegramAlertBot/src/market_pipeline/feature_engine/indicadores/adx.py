

import statistics


def calculate_adx(candles, period=14):
    """
    Calcula ADX + DI+ / DI- (feature pura, sin interpretación)
    """

    if not candles or len(candles) < period + 25:
        return None

    tr, plus_dm, minus_dm = [], [], []

    for i in range(1, len(candles)):
        h = candles[i]["high"]
        l = candles[i]["low"]
        cp = candles[i - 1]["close"]

        # True Range
        tr.append(max(h - l, abs(h - cp), abs(l - cp)))

        # Directional Movement
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
    if size == 0:
        return None

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
        return None

    adx = sum(dx[-period:]) / period

    # promedio reciente de DI para dirección
    plus_avg = statistics.mean(plus_s[-10:])
    minus_avg = statistics.mean(minus_s[-10:])

    return {
        "adx": adx,
        "plus_di": plus_avg,
        "minus_di": minus_avg,
        "strength": adx / 100  # normalizado 0–1
    }


def analyze_adx(adx_data):
    """
    Interpretación del ADX (señal)
    """

    if adx_data is None:
        return None

    adx = adx_data["adx"]
    plus = adx_data["plus_di"]
    minus = adx_data["minus_di"]

    # filtro de mercado sin tendencia
    if adx < 20:
        return None

    # dirección
    trend = "bullish" if plus > minus else "bearish"

    # fuerza
    if adx > 40:
        strength = 1.0
    elif adx > 30:
        strength = 0.8
    else:
        strength = 0.5

    return {
        "indicator": "ADX",
        "signal": trend,
        "strength": strength,
        "adx": adx
    }

