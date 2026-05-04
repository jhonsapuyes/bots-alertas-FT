

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


def run_opportunity_engine(features: dict, regime: dict):
    """
    Opportunity Engine

    INPUT:
        features (feature_engine)
        regime (regime_engine)

    OUTPUT:
        opportunities: list[dict]
    """

    opportunities = []

    # =========================
    # CONTEXTO BASE
    # =========================
    context = {
        "features": features,
        "regime": regime
    }

    # =========================
    # EJECUTAR DETECTORES
    # =========================
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

    for detector in detectors:
        try:
            result = detector(context)

            if result:
                # puede devolver dict o lista
                if isinstance(result, list):
                    opportunities.extend(result)
                else:
                    opportunities.append(result)

        except Exception as e:
            print(f"[ERROR] Detector {detector.__name__}: {e}")

    # =========================
    # FILTRADO BÁSICO
    # =========================
    opportunities = _filter_opportunities(opportunities)

    # =========================
    # ORDENAR POR SCORE
    # =========================
    opportunities.sort(key=lambda x: x.get("score", 0), reverse=True)

    return opportunities


# =========================
# FILTROS
# =========================
def _filter_opportunities(opps: list):
    """
    Limpia oportunidades basura
    """

    clean = []

    for opp in opps:

        # evitar estructuras vacías
        if not isinstance(opp, dict):
            continue

        # debe tener tipo
        if "type" not in opp:
            continue

        # score mínimo
        if opp.get("score", 0) < 0.5:
            continue

        clean.append(opp)

    return clean

