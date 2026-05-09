

# opportunity_engine.py
from .detectors.breakout_detector import detect_breakout
from .detectors.continuationMicro_detector import detect_continuation_micro
from .detectors.exhaustion_detector import detect_exhaustion
from .detectors.liquidity_grab_detector import detect_liquidity_grab
from .detectors.mean_reversion_detector import detect_mean_reversion
from .detectors.microRange_detector import detect_micro_range
from .detectors.momentum_ignition_detector import detect_momentum_ignition
from .detectors.pullback_detector import detect_pullback
from .detectors.range_detector import detect_range
from .detectors.reversal_detector import detect_reversal
from .detectors.trend_detector import detect_trend
from .detectors.volatility_expansion_detector import detect_volatility_expansion


# =========================================================
# NORMALIZADOR INTERNO
# =========================================================
def _normalize(opportunity: dict, regime: dict):

    score = opportunity.get("score", 0.5)

    return {
        "type": opportunity.get("type"),
        "direction": opportunity.get("direction") or opportunity.get("side"),
        "valid": bool(opportunity.get("detected", True)),
        "strength": _map_score_to_strength(score),
        "score": round(score, 3),
        "regime": regime.get("market_regime"),
        "reason": opportunity.get("reason", ""),
    }


def _map_score_to_strength(score):
    if score >= 0.75:
        return "strong"
    elif score >= 0.6:
        return "medium"
    return "weak"


# =========================================================
# REGIME BOOST
# =========================================================
def apply_regime_boost(opportunity: dict, regime: dict):

    score = opportunity["score"]
    opp_type = opportunity["type"]
    market_regime = regime.get("market_regime")

    if market_regime == "transition":

        if opp_type in ["liquidity_grab", "exhaustion", "volatility_expansion"]:
            score += 0.12

        if opp_type == "micro_range":
            score -= 0.05

    elif market_regime == "trend":

        if opp_type in ["breakout", "pullback", "continuation_micro"]:
            score += 0.12

        if opp_type in ["mean_reversion", "micro_range"]:
            score -= 0.08

    elif market_regime == "range":

        if opp_type in ["mean_reversion", "micro_range"]:
            score += 0.12

        if opp_type == "breakout":
            score -= 0.1

    opportunity["score"] = max(0.1, min(score, 1.0))
    opportunity["strength"] = _map_score_to_strength(opportunity["score"])

    return opportunity


# =========================================================
# 🔥 SIGNAL TRANSLATOR (mejora direction si falta)
# =========================================================
def translate_signal(opportunity: dict, features: dict, regime: dict):

    if opportunity.get("direction"):
        return opportunity

    pressure = regime.get("pressure")
    trend_dir = features.get("trend", {}).get("trend_direction")

    direction = "neutral"

    if pressure == "bullish" or trend_dir == "bullish":
        direction = "long"

    elif pressure == "bearish" or trend_dir == "bearish":
        direction = "short"

    opportunity["direction"] = direction
    return opportunity


# =========================================================
# 🔥 FINAL SIGNAL FORMAT (LO QUE TÚ QUIERES)
# =========================================================
def _finalize_signal(opportunity: dict):

    return {
        "type": opportunity["type"],
        "direction": opportunity.get("direction", "neutral"),
        "valid": opportunity.get("valid", True),
        "strength": opportunity.get("strength", "weak"),
    }


# =========================================================
# ENGINE PRINCIPAL
# =========================================================
def run_opportunity_engine(features: dict, regime: dict):

    opportunities = []

    context = {
        "features": features,
        "regime": regime
    }

    detectors = [
        detect_trend,
        detect_pullback,
        detect_breakout,
        detect_range,
        detect_reversal,
        detect_exhaustion,
        detect_liquidity_grab,
        detect_mean_reversion,
        detect_momentum_ignition,
        detect_volatility_expansion,
        detect_micro_range,
        detect_continuation_micro,
    ]

    # =========================
    # DETECTORES
    # =========================
    for detector in detectors:
        try:
            result = detector(context)

            if not result:
                continue

            if isinstance(result, list):
                for r in result:
                    opportunities.append(_normalize(r, regime))
            else:
                opportunities.append(_normalize(result, regime))

        except Exception as e:
            print(f"[ERROR] {detector.__name__}: {e}")

    # =========================
    # FILTRO
    # =========================
    opportunities = [
        opp for opp in opportunities
        if opp.get("type") and opp.get("score", 0) >= 0.45
    ]

    # =========================
    # BOOST
    # =========================
    opportunities = [
        apply_regime_boost(opp, regime)
        for opp in opportunities
    ]

    # =========================
    # TRANSLATE
    # =========================
    opportunities = [
        translate_signal(opp, features, regime)
        for opp in opportunities
    ]

    # =========================
    # FINAL OUTPUT CLEAN (🔥 IMPORTANTE)
    # =========================
    final_opportunities = [
        _finalize_signal(opp)
        for opp in opportunities
    ]

    # orden opcional (aunque ya no tienes score en output final)
    return final_opportunities

