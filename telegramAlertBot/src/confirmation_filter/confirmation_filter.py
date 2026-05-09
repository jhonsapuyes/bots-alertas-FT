def evaluate_confirmation(data):
    features = data["features"]
    regime = data["regime"]
    signal = data["signal"]
    opportunity = data["opportunity"]

    trend = features["trend"]
    momentum = features["momentum"]
    volatility = features["volatility"]

    timestamp = signal.get("timestamp", 0)

    # 🔥 CONTEXTO CLAVE
    is_range = regime["market_regime"] == "range"

    # 🔥 NUEVO
    signal_bias = _normalize_bias(signal.get("bias"))

    setup_confirmed = False
    trade_confirmed = False

    # -------------------------
    # HARD FILTERS
    # -------------------------
    if regime["market_regime"] == "transition":
        return _build_full_output(
            confirmed=False,
            state="rejected",
            confidence=0.25,
            permission="blocked",
            priority="low",
            mode="skip",
            bias="none",
            quality="D",
            label="noise",
            size=0.0,
            risk_pct=0.0,
            aggression="low",
            entry="limit",
            validity="short",
            scale=False,
            reasons=["market in transition regime"],
            regime_name=regime["market_regime"],
            signal_type=signal["type"],
            timestamp=timestamp,
            setup_confirmed=False,
            trade_confirmed=False
        )

    # -------------------------
    # SCORING
    # -------------------------

    # TREND
    trend_score = 0.5

    if trend["trend_direction"] == signal.get("bias"):
        trend_score += 0.15

    if trend["trend_strength"] == "weak":
        trend_score -= 0.03

    # -------------------------
    # MOMENTUM
    # -------------------------
    momentum_state = momentum.get("momentum_state", "neutral")
    momentum_strength = momentum.get("momentum_strength", "weak")

    if momentum_state == "neutral":

        momentum_score = 0.5

        # intensidad sin dirección
        if momentum_strength == "strong":
            momentum_score += 0.05

    elif momentum_state in ["bullish", "bearish"]:

        momentum_score = 0.65

        if momentum_strength == "strong":
            momentum_score += 0.1

    else:
        momentum_score = 0.4

    # -------------------------
    # REGIME FIT
    # -------------------------
    regime_map = {
        "trend": 0.75,
        "weak_trend": 0.65,
        "range": 0.6,
        "transition": 0.4
    }

    regime_score = regime_map.get(
        regime["market_regime"],
        0.5
    )

    # micro-range bonus
    if (
        signal["type"] == "micro_range"
        and regime["market_regime"] in ["range", "weak_trend"]
    ):
        regime_score += 0.05

    # -------------------------
    # VOLATILITY
    # -------------------------
    vol_map = {
        "low": 0.55,
        "medium": 0.6,
        "high": 0.55
    }

    volatility_score = vol_map.get(
        volatility["volatility_level"],
        0.55
    )

    # -------------------------
    # SIGNAL
    # -------------------------
    signal_score = signal["confidence"] * 0.8 + 0.2

    # -------------------------
    # FINAL SCORE
    # -------------------------
    confidence_score = round((
        trend_score * 0.25 +
        momentum_score * 0.20 +
        regime_score * 0.25 +
        volatility_score * 0.10 +
        signal_score * 0.20
    ), 3)

    # =====================================================
    # SETUP VALIDATION
    # =====================================================

    if confidence_score >= 0.60:

        # 🔥 CAMBIO SEMÁNTICO
        state = "setup_valid"

        setup_confirmed = True

        quality = "A"
        label = "institutional"

        size = 1.0
        risk_pct = 1.0

        aggression = "high"
        entry = "market"
        validity = "immediate"
        scale = True

    elif confidence_score >= 0.52:

        # 🔥 CAMBIO SEMÁNTICO
        state = "setup_valid"

        setup_confirmed = True

        quality = "B"
        label = "solid"

        size = 0.75
        risk_pct = 0.75

        aggression = "medium"
        entry = "limit"
        validity = "short"
        scale = True

    elif confidence_score >= (0.45 if is_range else 0.48):

        # 🔥 CAMBIO SEMÁNTICO
        state = "setup_weak"

        quality = "C"
        label = "marginal"

        size = 0.4
        risk_pct = 0.5

        aggression = "low"
        entry = "limit"
        validity = "short"
        scale = False

    else:

        state = "rejected"

        quality = "D"
        label = "noise"

        size = 0.0
        risk_pct = 0.0

        aggression = "low"
        entry = "limit"
        validity = "short"
        scale = False

    # =====================================================
    # TRADE EXECUTABILITY
    # =====================================================

    trade_confirmed = (
        setup_confirmed
        and signal_bias != "none"
    )

    # 🔥 FIX SEMÁNTICO
    # no se puede escalar un trade no ejecutable
    if not trade_confirmed:
        scale = False

    # =====================================================
    # EXECUTION DECISION
    # =====================================================

    if trade_confirmed:

        confirmed = True

        if confidence_score >= 0.60:
            permission = "allowed"
            priority = "high"
            mode = "aggressive"

        else:
            permission = "allowed"
            priority = "medium"
            mode = "passive"

    else:

        confirmed = False

        if setup_confirmed:
            permission = "reduced"
            priority = "low"
            mode = "passive"

        else:
            permission = "blocked"
            priority = "low"
            mode = "skip"

    # 🔥 coherencia total
    bias = signal_bias if trade_confirmed else "none"

    return _build_full_output(
        confirmed=confirmed,
        state=state,
        confidence=confidence_score,
        permission=permission,
        priority=priority,
        mode=mode,
        bias=bias,
        quality=quality,
        label=label,
        size=size,
        risk_pct=risk_pct,
        aggression=aggression,
        entry=entry,
        validity=validity,
        scale=scale,
        reasons=_build_reasons(
            trend,
            momentum,
            regime,
            signal
        ),
        regime_name=regime["market_regime"],
        signal_type=signal["type"],
        timestamp=timestamp,
        trend_score=trend_score,
        momentum_score=momentum_score,
        regime_score=regime_score,
        volatility_score=volatility_score,
        signal_score=signal_score,

        # 🔥 NUEVO
        setup_confirmed=setup_confirmed,
        trade_confirmed=trade_confirmed
    )


# =====================================================
# OUTPUT BUILDER
# =====================================================

def _build_full_output(
    confirmed,
    state,
    confidence,
    permission,
    priority,
    mode,
    bias,
    quality,
    label,
    size,
    risk_pct,
    aggression,
    entry,
    validity,
    scale,
    reasons,
    regime_name,
    signal_type,
    timestamp,

    trend_score=0,
    momentum_score=0,
    regime_score=0,
    volatility_score=0,
    signal_score=0,

    setup_confirmed=False,
    trade_confirmed=False
):
    return {
        "confirmed": confirmed,

        # 🔥 MISMA KEY
        # 🔥 NUEVA SEMÁNTICA
        "signal_state": state,

        "confidence_score": confidence,

        "execution": {
            "permission": permission,
            "priority": priority,
            "mode": mode
        },

        "position_bias": bias,

        "quality": {
            "tier": quality,
            "label": label
        },

        "edge_components": {
            "trend_alignment": round(trend_score, 2),
            "momentum_confirmation": round(momentum_score, 2),
            "regime_fit": round(regime_score, 2),
            "volatility_suitability": round(volatility_score, 2),
            "signal_integrity": round(signal_score, 2)
        },

        "risk": {
            "size_multiplier": size,
            "max_risk_pct": risk_pct,
            "aggression_level": aggression
        },

        "trade_management": {
            "entry_style": entry,
            "time_validity": validity,
            "scale_in_allowed": scale
        },

        "reasons": reasons,

        "invalidations": (
            ["no trade"]
            if permission == "blocked"
            else [
                "structure break against position",
                "opposite pressure expansion",
                "volatility spike against setup"
            ]
        ),

        "meta": {
            "regime": regime_name,
            "signal_type": signal_type,
            "timestamp": timestamp,

            # 🔥 NUEVO
            "setup_confirmed": setup_confirmed,
            "trade_confirmed": trade_confirmed
        }
    }


def _normalize_bias(bias):
    return bias if bias in ["long", "short"] else "none"


def _build_reasons(trend, momentum, regime, signal):

    reasons = []

    if trend["trend_strength"] == "weak":
        reasons.append("weak trend reduces conviction")

    if momentum["momentum_state"] == "neutral":
        reasons.append("momentum not confirming direction")

    if regime["market_regime"] == "weak_trend":
        reasons.append("limited expansion regime")

    if signal["confidence"] < 0.6:
        reasons.append("signal confidence not strong")

    return reasons

