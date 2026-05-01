

from market_pipeline.data_fetch.get_market_data import get_market_data

from market_pipeline.feature_engine.indicadores.sma import calculate_sma, analyze_sma
from market_pipeline.feature_engine.indicadores.rsi import calculate_rsi, analyze_rsi
from market_pipeline.feature_engine.indicadores.macd import calculate_macd, analyze_macd

from market_pipeline.feature_engine.indicadores.adx import calculate_adx, analyze_adx
from market_pipeline.feature_engine.indicadores.obv import calculate_obv, analyze_obv
from market_pipeline.feature_engine.indicadores.bollinger import calculate_bollinger, analyze_bollinger

def analyzeData(symbol):

    candles = get_market_data(symbol)
    print("analyzeData:", candles)
    print("analyzeData:", )


    if not candles or len(candles) < 50:
        return {"symbol": symbol, "error": "not enough data"}

    prices = [c["close"] for c in candles]
    price = prices[-1]

    # =========================
    # INDICATORS
    # =========================

    sma = calculate_sma(prices)
    rsi = calculate_rsi(prices)
    macd, signal = calculate_macd(prices)
    adx_val, trend = calculate_adx(candles)
    obv_raw = calculate_obv(candles)
    upper, mid, lower, bandwidth = calculate_bollinger(candles)

    # =========================
    # SIGNALS
    # =========================

    sma_signal = analyze_sma(price, sma)
    rsi_signal = analyze_rsi(rsi)
    macd_signal = analyze_macd(macd, signal)
    adx_signal = analyze_adx(adx_val, trend)
    obv_signal = analyze_obv(obv_raw)
    boll_signal = analyze_bollinger(price, upper, lower)

    signals = [
        s for s in [
            sma_signal,
            rsi_signal,
            macd_signal,
            adx_signal,
            obv_signal,
            boll_signal
        ] if s is not None
    ]

    # =========================
    # 🧠 NEW: MOMENTUM ENGINE
    # =========================

    macd_hist = macd - signal
    sma_diff = price - sma

    # tendencia direccional real
    bullish_pressure = 0
    bearish_pressure = 0

    if price > sma:
        bullish_pressure += 1
    else:
        bearish_pressure += 1

    if macd_hist > 0:
        bullish_pressure += 1
    else:
        bearish_pressure += 1

    if rsi > 55:
        bullish_pressure += 1
    elif rsi < 45:
        bearish_pressure += 1

    if adx_val > 25:
        bullish_pressure += 0.5  # trend strength bonus

    # =========================
    # 📊 MARKET PHASE
    # =========================

    if adx_val < 20:
        market_phase = "range"
    elif adx_val >= 20 and adx_val < 30:
        market_phase = "trend_building"
    else:
        market_phase = "strong_trend"

    # =========================
    # 📈 TREND STRENGTH SCORE
    # =========================

    trend_strength = bullish_pressure - bearish_pressure

    if trend_strength >= 2:
        momentum = "bullish"
    elif trend_strength <= -2:
        momentum = "bearish"
    else:
        momentum = "neutral"

    # =========================
    # FINAL OUTPUT
    # =========================

    return {
        "symbol": symbol,
        "price": price,

        # indicators
        "sma": sma,
        "rsi": rsi,
        "macd": macd,
        "signal": signal,
        "adx": adx_val,
        "trend": trend,
        "volatility": bandwidth,

        # signals
        "signals": signals,

        # 🧠 NEW INTELLIGENCE LAYER
        "market_phase": market_phase,
        "momentum": momentum,
        "trend_strength": trend_strength,
        "macd_hist": macd_hist
    }

