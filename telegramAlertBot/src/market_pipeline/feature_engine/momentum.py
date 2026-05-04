

def calculate_momentum1(candles, period=5):

    if len(candles) < period + 1:
        return {"momentum": "neutral"}

    closes = [c["close"] for c in candles]

    # 🔹 MOMENTUM SIMPLE (precio actual vs pasado)
    momentum_value = closes[-1] - closes[-period]

    # 🔹 RSI SIMPLE
    gains = []
    losses = []

    for i in range(1, len(closes)):
        diff = closes[i] - closes[i - 1]

        if diff > 0:
            gains.append(diff)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(diff))

    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period

    if avg_loss == 0:
        rsi = 100
    else:
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

    # 🔥 INTERPRETACIÓN
    if rsi > 70:
        momentum_state = "overbought"
    elif rsi < 30:
        momentum_state = "oversold"
    elif momentum_value > 0:
        momentum_state = "bullish"
    elif momentum_value < 0:
        momentum_state = "bearish"
    else:
        momentum_state = "neutral"

    return {
        "momentum": momentum_state,
        "rsi": rsi,
        "momentum_value": momentum_value
    }


from .indicadores.indicator_engine import calculate_indicators


def calculate_momentum(candles, indicators=None, period=5):

    if len(candles) < period + 1:
        return {"momentum": "neutral"}

    # 🔥 usar indicadores (no recalcular)
    indicators = indicators or calculate_indicators(candles)

    closes = [c["close"] for c in candles]

    # 🔹 momentum simple
    momentum_value = closes[-1] - closes[-period]

    # 🔹 RSI desde indicator_engine
    rsi = indicators.get("rsi", {}).get("value")

    # 🔹 MACD opcional (extra señal)
    macd_state = indicators.get("macd", {}).get("state")

    # 🔥 interpretación mejorada
    if rsi is not None:
        if rsi > 70:
            momentum_state = "overbought"
        elif rsi < 30:
            momentum_state = "oversold"
        elif momentum_value > 0:
            momentum_state = "bullish"
        elif momentum_value < 0:
            momentum_state = "bearish"
        else:
            momentum_state = "neutral"
    else:
        momentum_state = "neutral"

    return {
        "momentum": momentum_state,
        "rsi": rsi,
        "momentum_value": momentum_value,
        "macd_state": macd_state
    }

