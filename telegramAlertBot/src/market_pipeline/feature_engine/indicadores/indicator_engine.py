

# feature_engine/indicadores/indicator_engine.py

from .rsi import calculate_rsi
from .macd import calculate_macd
from .ema import calculate_ema
from .adx import calculate_adx
from .bollinger import calculate_bollinger
from .obv import calculate_obv
from .sma import calculate_sma


def calculate_indicators(candles, cache=None):

    if cache is not None:
        return cache

    if not candles or len(candles) < 2:
        return {}

    closes = [c["close"] for c in candles]
    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]
    volumes = [c["volume"] for c in candles]

    indicators = {}

    # =========================
    # RSI
    # =========================
    try:
        rsi = calculate_rsi(closes)

        if rsi is not None:
            if rsi > 70:
                state = "overbought"
            elif rsi < 30:
                state = "oversold"
            else:
                state = "neutral"
        else:
            state = None

        indicators["rsi"] = {
            "value": rsi,
            "state": state
        }
    except Exception:
        indicators["rsi"] = {"value": None, "state": None}

    # =========================
    # MACD
    # =========================
    try:
        macd = calculate_macd(closes)

        macd_line = macd.get("macd")
        signal = macd.get("signal")

        if macd_line is not None and signal is not None:
            if macd_line > signal:
                macd_state = "bullish"
            else:
                macd_state = "bearish"
        else:
            macd_state = None

        indicators["macd"] = {
            "macd": macd_line,
            "signal": signal,
            "state": macd_state
        }
    except Exception:
        indicators["macd"] = {"macd": None, "signal": None, "state": None}

    # =========================
    # EMA + SMA (trend bias)
    # =========================
    try:
        ema_fast = calculate_ema(closes, period=9)
        ema_slow = calculate_ema(closes, period=21)
        sma = calculate_sma(closes, period=20)

        if ema_fast and ema_slow:
            if ema_fast > ema_slow:
                trend_bias = "bullish"
            else:
                trend_bias = "bearish"
        else:
            trend_bias = None

        indicators["trend_ma"] = {
            "ema_fast": ema_fast,
            "ema_slow": ema_slow,
            "sma": sma,
            "bias": trend_bias
        }
    except Exception:
        indicators["trend_ma"] = {
            "ema_fast": None,
            "ema_slow": None,
            "sma": None,
            "bias": None
        }

    # =========================
    # ADX
    # =========================
    try:
        adx = calculate_adx(highs, lows, closes)

        if adx is not None:
            if adx > 25:
                strength = "strong"
            else:
                strength = "weak"
        else:
            strength = None

        indicators["adx"] = {
            "value": adx,
            "strength": strength
        }
    except Exception:
        indicators["adx"] = {"value": None, "strength": None}

    # =========================
    # Bollinger
    # =========================
    try:
        bb = calculate_bollinger(closes)

        upper = bb.get("upper")
        lower = bb.get("lower")
        middle = bb.get("middle")
        last_price = closes[-1]

        if upper and lower:
            if last_price > upper:
                position = "above_band"
            elif last_price < lower:
                position = "below_band"
            else:
                position = "inside"
        else:
            position = None

        indicators["bollinger"] = {
            "upper": upper,
            "lower": lower,
            "middle": middle,
            "position": position
        }
    except Exception:
        indicators["bollinger"] = {
            "upper": None,
            "lower": None,
            "middle": None,
            "position": None
        }

    # =========================
    # OBV
    # =========================
    try:
        obv = calculate_obv(closes, volumes)

        indicators["obv"] = {
            "value": obv,
            "direction": "up" if obv and obv > 0 else "down"
        }
    except Exception:
        indicators["obv"] = {"value": None, "direction": None}

    return indicators

