

from strategy.opportunityDetect_range import opportunityDetect_range
from strategy.opportunityDetect_trend import opportunityDetect_trend
from strategy.opportunityDetect_breakout import opportunityDetect_breakout
from strategy.opportunityDetect_exhaustion import opportunityDetect_exhaustion
from strategy.opportunityDetect_pullback import opportunityDetect_pullback
from strategy.opportunityDetect_reversal import opportunityDetect_reversal


def marketCore(context):

    analysis = context["analysis"]
    data = context["data"]
    bias = context["bias"]
    fatigue = context["fatigue"]

    detectors = {
        "range": opportunityDetect_range,
        "trend": opportunityDetect_trend,
        "breakout": opportunityDetect_breakout,
        "pullback": opportunityDetect_pullback,
        "reversal": opportunityDetect_reversal,
        "exhaustion": opportunityDetect_exhaustion
    }

    market_state = context["market_state"]

    scenarios = {}

    for name, detector in detectors.items():

        try:
            result = detector(analysis, data) if True else {}

            scenario = {
                "type": name,
                "active": False,
                "score": 0,
                "confidence": 0,
                "weight": 1.0,
                "valid": False
            }

            if not isinstance(result, dict):
                scenarios[name] = scenario
                continue

            adx = analysis.get("adx", 0)
            vol = analysis.get("volatility", 0)
            trend = analysis.get("trend")

            # =========================
            # 🧠 VALIDACIÓN DE MERCADO (CLAVE)
            # =========================
            valid_map = {
                "range": adx < 18,
                "trend": adx > 22,
                "breakout": vol > 0.02,
                "pullback": trend in ["bullish", "bearish"],
                "reversal": adx < 25,
                "exhaustion": adx > 20
            }

            scenario["valid"] = valid_map.get(name, True)

            if not scenario["valid"]:
                scenarios[name] = scenario
                continue

            scenario.update(result)

            base_score = result.get("score", 0)

            weight = 1.0

            if name == "breakout" and vol > 0.02:
                weight = 1.6
            elif name == "trend" and adx > 25:
                weight = 1.5
            elif name == "range" and adx < 18:
                weight = 1.4

            # =========================
            # 🧠 CONTEXTO BIAS
            # =========================
            if market_state == "range" and name == "range":
                weight *= 1.2

            if market_state == "breakout" and name == "breakout":
                weight *= 1.2

            # =========================
            # 🔥 FATIGA
            # =========================
            if fatigue:
                phase = fatigue.get("phase")

                if phase == "exhaustion" and name == "reversal":
                    weight *= 1.3
                elif phase == "mature":
                    weight *= 0.9

            score = base_score * weight

            scenario.update({
                "weight": weight,
                "score": score,
                "confidence": min(1.0, score / 10),
                "active": score > 1.2
            })

            scenarios[name] = scenario

        except Exception as e:
            scenarios[name] = {
                "type": name,
                "active": False,
                "score": 0,
                "error": str(e)
            }

    return scenarios

