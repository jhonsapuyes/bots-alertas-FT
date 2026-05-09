

def translate_signal1(opportunity: dict, features: dict, regime: dict):
    """
    Convierte una oportunidad en una señal operable para strategy_engine
    OUTPUT: SIGNAL TRANSLATOR v2 (production-ready)
    """

    opp_type = opportunity.get("type")
    score = opportunity.get("score", 0)
    opp_direction = opportunity.get("direction")

    trend = features.get("trend", {})
    volatility = features.get("volatility", {})
    price = features.get("price", {})

    market_regime = regime.get("market_regime")
    pressure = regime.get("pressure")

    trend_direction = trend.get("trend_direction")
    trend_strength = trend.get("trend_strength")

    # =========================
    # ALIGNMENT CALCULATION
    # =========================
    trend_alignment = (
        (opp_direction == "long" and trend_direction == "bullish") or
        (opp_direction == "short" and trend_direction == "bearish")
    )

    # =========================
    # BASE SIGNAL
    # =========================
    signal = {
        "type": opp_type,
        "bias": "neutral",
        "confidence": round(score, 2),

        "context": {
            "regime": market_regime,
            "pressure": pressure,
            "trend_alignment": trend_alignment
        },

        "invalidations": {},
        "execution_hints": {}
    }

    # =========================
    # BIAS ENGINE
    # =========================
    if market_regime in ["weak_trend", "trend"]:

        if pressure == "bullish" and trend_direction == "bullish":
            signal["bias"] = "long"

        elif pressure == "bearish" and trend_direction == "bearish":
            signal["bias"] = "short"

    elif market_regime in ["range", "transition"]:

        if opp_type in ["micro_range", "mean_reversion"]:
            signal["bias"] = "range_reversion"

        elif opp_type in ["breakout", "volatility_expansion"]:
            signal["bias"] = "neutral"

    # =========================
    # INVALIDATIONS (SIMPLIFIED)
    # =========================
    signal["invalidations"] = {
        "structure_break": (
            trend_strength == "weak" and opp_type == "breakout"
        ),

        "opposite_pressure": (
            "bearish_spike"
            if (pressure == "bearish" and opp_direction == "long")
            else None
        )
    }

    # =========================
    # EXECUTION HINTS
    # =========================
    signal["execution_hints"] = {
        "aggression": "low" if score < 0.6 else "medium",

        "entry_style": (
            "limit_pullback" if opp_type == "pullback"
            else "limit_reversion" if opp_type in ["micro_range", "mean_reversion"]
            else "market_breakout"
        ),

        "avoid": [
            "chop" if market_regime == "range" else None,
            "low_volume" if volatility.get("volatility_level") == "low" else None
        ]
    }

    # limpiar Nones
    signal["execution_hints"]["avoid"] = [
        x for x in signal["execution_hints"]["avoid"] if x is not None
    ]

    return signal


def translate_signal(opportunity: dict, features: dict, regime: dict):
    """
    Signal Translator v5 - production-ready decision layer
    """

    opp_type = opportunity.get("type")
    opp_direction = opportunity.get("direction")

    trend = features.get("trend", {})
    volatility = features.get("volatility", {})
    price = features.get("price", {})

    market_regime = regime.get("market_regime")
    pressure = regime.get("pressure")

    trend_direction = trend.get("trend_direction")
    trend_strength = trend.get("trend_strength")
    structure_score = trend.get("structure_score", 0)

    # =========================
    # ALIGNMENT
    # =========================
    trend_alignment = (
        (opp_direction == "long" and trend_direction == "bullish") or
        (opp_direction == "short" and trend_direction == "bearish")
    )

    # =========================
    # CONFIDENCE (REALISTIC SCORING 0–1)
    # =========================
    confidence = round(
        min(1.0,
            (structure_score / 100) * 0.5 +
            (0.25 if trend_alignment else 0.10) +
            (0.2 if pressure in ["bullish", "bearish"] else 0.1) +
            (0.1 if volatility.get("volatility_level") == "medium" else 0.05)
        ),
        3
    )

    # =========================
    # BASE SIGNAL
    # =========================
    signal = {
        "type": opp_type,
        "bias": "neutral",
        "confidence": confidence,

        "context": {
            "regime": market_regime,
            "pressure": pressure,
            "trend_alignment": trend_alignment
        },

        "invalidations": {},
        "execution_hints": {}
    }

    # =========================
    # BIAS ENGINE
    # =========================
    if market_regime in ["weak_trend", "trend"]:

        if pressure == "bullish" and trend_direction == "bullish":
            signal["bias"] = "long"

        elif pressure == "bearish" and trend_direction == "bearish":
            signal["bias"] = "short"

    elif market_regime in ["range", "transition"]:

        signal["bias"] = (
            "range_reversion"
            if opp_type in ["micro_range", "mean_reversion"]
            else "neutral"
        )

    # =========================
    # STRUCTURE BREAK (REALISTIC MODEL)
    # =========================
    structure_break = (
        trend_strength == "weak"
        and volatility.get("volatility_level") == "high"
        and not trend_alignment
    )

    signal["invalidations"]["structure_break"] = structure_break

    # =========================
    # OPPOSITE PRESSURE (MEANINGFUL)
    # =========================
    if pressure == "bullish":
        opposite_pressure = "bullish_dominance"
    elif pressure == "bearish":
        opposite_pressure = "bearish_dominance"
    else:
        opposite_pressure = "no_pressure"

    signal["invalidations"]["opposite_pressure"] = opposite_pressure

    # =========================
    # EXECUTION HINTS (FULL COVERAGE)
    # =========================
    avoid = []

    if market_regime == "range":
        avoid.append("choppy_market")

    if volatility.get("volatility_level") == "low":
        avoid.append("low_momentum")

    if not trend_alignment:
        avoid.append("trend_conflict")

    if structure_break:
        avoid.append("structure_instability")

    if confidence < 0.6:
        avoid.append("weak_edge")

    signal["execution_hints"] = {
        "aggression": "low" if confidence < 0.6 else "medium",

        "entry_style": (
            "limit_pullback" if opp_type == "pullback"
            else "limit_reversion" if opp_type in ["micro_range", "mean_reversion"]
            else "market_breakout"
        ),

        "avoid": avoid
    }

    return signal

