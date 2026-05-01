

from strategy.opportunityDetect_meanReversion import opportunityDetect_meanReversion
from strategy.opportunityDetect_momentumIgnition import opportunityDetect_momentumIgnition
from strategy.opportunityDetect_microRange import opportunityDetect_microRange
from strategy.opportunityDetect_continuationMicro import opportunityDetect_continuationMicro
from strategy.opportunityDetect_volatilityExpansion import opportunityDetect_volatilityExpansion
from strategy.opportunityDetect_liquidityGrab import opportunityDetect_liquidityGrab


def marketMicro(context):

    analysis = context["analysis"]
    data = context["data"]
    bias = context["bias"]
    fatigue = context["fatigue"]

    market_state = context["market_state"]

    detectors = {
        "mean_reversion": opportunityDetect_meanReversion,
        "momentum_ignition": opportunityDetect_momentumIgnition,
        "micro_range": opportunityDetect_microRange,
        "continuation_micro": opportunityDetect_continuationMicro,
        "volatility_expansion": opportunityDetect_volatilityExpansion,
        "liquidity_grab": opportunityDetect_liquidityGrab
    }

    # 🔥 ROUTING REAL
    allowed = {
        "range": ["mean_reversion", "liquidity_grab", "micro_range"],
        "trend": ["continuation_micro", "momentum_ignition"],
        "breakout": ["volatility_expansion"],
        "reversal": ["liquidity_grab", "mean_reversion"]
    }

    valid = allowed.get(market_state, [])

    scenarios = {}

    for name, detector in detectors.items():

        # 🚫 filtro crítico
        if name not in valid:
            continue

        try:
            result = detector(analysis, data)

            scenario = {
                "type": name,
                "active": False,
                "score": 0,
                "confidence": 0,
                "weight": 1.0
            }

            if not isinstance(result, dict):
                scenarios[name] = scenario
                continue

            adx = analysis.get("adx", 0)
            vol = analysis.get("volatility", 0)

            scenario.update(result)

            base_score = result.get("score", 0)

            weight = 1.0

            if name == "momentum_ignition" and vol > 0.015:
                weight = 1.6
            elif name == "liquidity_grab":
                weight = 1.4
            elif name == "mean_reversion" and adx < 18:
                weight = 1.3

            # 🔥 FATIGA
            if fatigue:
                if fatigue.get("phase") == "exhaustion":
                    weight *= 1.2

            score = base_score * weight

            scenario.update({
                "weight": weight,
                "score": score,
                "confidence": min(1.0, score / 8),
                "active": score > 1
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

