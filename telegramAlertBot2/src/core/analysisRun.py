
from core.analyzeData import analyzeData
from strategy.combineSignals import combine_signals
from strategy.market_bias import market_bias
from execution.trend_fatigue_detector import TrendFatigueDetector

from core.marketCore import marketCore
from core.marketMicro import marketMicro

fatigue_detector = TrendFatigueDetector()


def analysisRun(symbol):

    data = analyzeData(symbol)
    print("analysisRun:", )
    print("analyzeData:", data)
    print("analysisRun:", )


    if "error" in data:
        return data

    signals = [s for s in data.get("signals", []) if s and "signal" in s]

    analysis = combine_signals(signals)

    analysis.update({
        "rsi": data.get("rsi"),
        "sma": data.get("sma"),
        "macd": data.get("macd"),
        "signal_line": data.get("signal"),
        "adx": data.get("adx"),
        "trend": data.get("trend"),
        "volatility": data.get("volatility"),
        "price": data.get("price")
    })

    # 🧠 1. BIAS (regime base)
    bias = market_bias(data)

    # 🔥 2. FATIGA
    fatigue = fatigue_detector.analyze(symbol, data)

    # 🧠 3. MARKET STATE (nuevo concepto clave)
    market_state = bias.get("scenario", "unknown")

    context = {
        "analysis": analysis,
        "data": data,
        "bias": bias,
        "fatigue": fatigue,
        "market_state": market_state
    }

    # =========================
    # 🧠 CORE
    # =========================
    core_scenarios = marketCore(context)

    # =========================
    # 🔬 MICRO
    # =========================
    micro_scenarios = marketMicro(context)

    return {
        "symbol": symbol,
        "analysis": analysis,
        "bias": bias,
        "fatigue": fatigue,
        "market_state": market_state,
        "layers": {
            "core": core_scenarios,
            "micro": micro_scenarios
        }
    } 

