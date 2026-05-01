

def normalize_candles(raw_candles):
    """
    Convierte data cruda de Binance a formato estándar del sistema
    """

    if not raw_candles:
        return []

    normalized = []

    for c in raw_candles:
        try:
            candle = {
                "timestamp": int(c["timestamp"]),
                "open": float(c["open"]),
                "high": float(c["high"]),
                "low": float(c["low"]),
                "close": float(c["close"]),
                "volume": float(c["volume"])
            }

            # validación mínima
            if (
                candle["high"] <= 0 or
                candle["low"] <= 0 or
                candle["close"] <= 0
            ):
                continue

            normalized.append(candle)

        except Exception:
            continue

    return normalized

