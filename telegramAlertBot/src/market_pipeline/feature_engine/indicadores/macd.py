

from market_pipeline.feature_engine.indicadores.ema import calculate_ema


def calculate_macd(prices):
    """
    MACD adaptado a EMA que devuelve valor único
    """

    if not prices or len(prices) < 35:
        return None, None

    macd_series = []

    # 🔥 reconstruimos la serie MACD manualmente
    for i in range(26, len(prices)):
        window = prices[:i+1]

        ema12 = calculate_ema(window, 12)
        ema26 = calculate_ema(window, 26)

        if ema12 is None or ema26 is None:
            continue

        macd_series.append(ema12 - ema26)

    if len(macd_series) < 9:
        return None, None

    signal = calculate_ema(macd_series, 9)

    return macd_series[-1], signal


def analyze_macd(macd, signal):
    """
    Señal de momentum basada en MACD
    """

    if macd is None or signal is None:
        return None

    diff = macd - signal
    scale = max(abs(macd), abs(signal), 1e-9)

    norm = diff / scale

    # filtro de ruido
    if abs(norm) < 0.05:
        return None

    return {
        "indicator": "MACD",
        "signal": "bullish" if norm > 0 else "bearish",
        "strength": min(abs(norm) * 5, 1.0)
    }