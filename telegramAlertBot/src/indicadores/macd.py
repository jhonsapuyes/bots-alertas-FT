

def ema(prices, period):
    k = 2 / (period + 1)
    ema_values = [prices[0]]

    for price in prices[1:]:
        ema_values.append(price * k + ema_values[-1] * (1 - k))

    return ema_values


def calculate_macd(prices):

    if len(prices) < 35:
        return None, None

    ema12 = ema(prices, 12)
    ema26 = ema(prices, 26)

    size = min(len(ema12), len(ema26))

    macd_line = [a - b for a, b in zip(ema12[-size:], ema26[-size:])]
    signal_line = ema(macd_line, 9)

    return macd_line[-1], signal_line[-1]


def analyze_macd(macd, signal):

    if macd is None or signal is None:
        return None

    diff = macd - signal
    scale = max(abs(macd), abs(signal), 1e-9)

    norm = diff / scale

    if abs(norm) < 0.05:
        return None  # 👈 elimina ruido

    return {
        "indicator": "MACD",
        "signal": "bullish" if norm > 0 else "bearish",
        "strength": min(abs(norm) * 5, 1.0)
    }

