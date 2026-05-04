

from .indicadores.indicator_engine import calculate_indicators


# =========================================================
# 1. RAW TREND CALCULATION (NO DECISIONS HERE)
# =========================================================
def calculate_trend(candles, indicators=None):

    if not candles or len(candles) < 3:
        return {
            "direction": "sideways",
            "structure_state": "sideways",
            "strength": "neutral",
            "ema_trend": None,
            "higher_highs": 0,
            "higher_lows": 0,
            "lower_highs": 0,
            "lower_lows": 0
        }

    indicators = indicators or calculate_indicators(candles)

    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]

    higher_highs = sum(highs[i] > highs[i - 1] for i in range(1, len(highs)))
    lower_highs = sum(highs[i] <= highs[i - 1] for i in range(1, len(highs)))

    higher_lows = sum(lows[i] > lows[i - 1] for i in range(1, len(lows)))
    lower_lows = sum(lows[i] <= lows[i - 1] for i in range(1, len(lows)))

    # STRUCTURE
    if higher_lows > lower_lows and higher_highs >= lower_highs:
        structure_state = "bullish"
    elif lower_highs > higher_highs and lower_lows >= higher_lows:
        structure_state = "bearish"
    elif higher_lows > lower_lows:
        structure_state = "bullish_recovery"
    elif lower_highs > higher_highs:
        structure_state = "bearish_recovery"
    else:
        structure_state = "sideways"

    # DIRECTION BASED ONLY ON STRUCTURE
    direction = (
        "bullish" if structure_state.startswith("bullish")
        else "bearish" if structure_state.startswith("bearish")
        else "sideways"
    )

    ema_fast = indicators.get("trend_ma", {}).get("ema_fast")
    ema_slow = indicators.get("trend_ma", {}).get("ema_slow")

    ema_trend = None
    if ema_fast is not None and ema_slow is not None:
        ema_trend = "bullish" if ema_fast > ema_slow else "bearish"

    adx = indicators.get("adx", {}).get("value")
    strength = "strong" if adx and adx > 25 else "weak"

    return {
        "direction": direction,
        "structure_state": structure_state,
        "strength": strength,
        "ema_trend": ema_trend,
        "higher_highs": higher_highs,
        "higher_lows": higher_lows,
        "lower_highs": lower_highs,
        "lower_lows": lower_lows
    }


