

def build_price_features(candles):

    if not candles:
        return {}

    last_candle = candles[-1]

    open_price = last_candle["open"]
    close_price = last_candle["close"]
    high_price = last_candle["high"]
    low_price = last_candle["low"]

    # 🔹 rango total de la vela
    candle_range = high_price - low_price

    # 🔹 cuerpo de la vela
    body = abs(close_price - open_price)

    # 🔹 dirección
    if close_price > open_price:
        direction = "bullish"
    elif close_price < open_price:
        direction = "bearish"
    else:
        direction = "neutral"

    return {
        "last_open": open_price,
        "last_close": close_price,
        "last_high": high_price,
        "last_low": low_price,
        "range": candle_range,
        "body": body,
        "direction": direction
    }

