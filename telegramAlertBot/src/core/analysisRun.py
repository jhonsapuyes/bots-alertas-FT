

from core.analyzeData import analyzeData
from strategy.combineSignals import combine_signals
from strategy.opportunity_detect_v1 import opportunity_detect_v1
from strategy.opportunity_detect_v2 import opportunity_detect_v2


def analysisRun(symbol):

    data = analyzeData(symbol)

    if "error" in data:
        return data

    signals = [s for s in data.get("signals", []) if s and "signal" in s]

    analysis = combine_signals(signals)

    analysis.update({
        "price": data.get("price"),
        "rsi": data.get("rsi"),
        "sma": data.get("sma"),
        "macd": data.get("macd"),
        "signal_line": data.get("signal"),
        "adx": data.get("adx"),
        "trend": data.get("trend"),
        "volatility": data.get("volatility")
    })

    ctx = {
        "analysis": analysis,
        "signals": signals,
        "data": data
    }

    # 🔥 CORRECTO: v1 = range | v2 = trend
    data["opportunity_v1"] = opportunity_detect_v1(ctx)
    data["opportunity_v2"] = opportunity_detect_v2(ctx)

    data["analysis"] = analysis

    return data

