

# risk_engine/engine.py

def build_risk(data):
    strategy_block = data["strategy"]
    confirmation = data["confirmation"]
    features = data["features"]
    regime = data["regime"]

    # -------------------------
    # CONTEXT EXTRACTION
    # -------------------------
    permission = confirmation["execution"]["permission"]
    mode = confirmation["execution"]["mode"]
    priority = confirmation["execution"]["priority"]

    risk_data = confirmation["risk"]
    aggression_level = risk_data["aggression_level"]
    max_risk_pct = risk_data["max_risk_pct"]
    size_multiplier = risk_data["size_multiplier"]

    regime_name = confirmation["meta"]["regime"]
    timestamp = confirmation["meta"].get("timestamp", 0)

    volatility = features["volatility"]["volatility_level"]
    avg_range = features["volatility"]["avg_range"]

    # -------------------------
    # HARD BLOCK
    # -------------------------
    if permission == "blocked" or not strategy_block["valid"]:
        return _build_output(
            valid=False,
            position_size=0.0,
            size_multiplier=0.0,
            max_risk_pct=0.0,
            estimated_loss=0.0,
            stop_type="none",
            stop_distance=0.0,
            atr_based=False,
            mode="skip",
            priority=priority,
            risk_profile="conservative",
            regime=regime_name,
            volatility=volatility,
            timestamp=timestamp,
            reasons=["trade blocked by confirmation"]
        )

    # -------------------------
    # POSITION SIZING
    # -------------------------
    base_size = _base_position_size(aggression_level)

    final_size = base_size * size_multiplier

    # clamp seguridad
    final_size = max(0.0, min(final_size, 1.0))

    # -------------------------
    # STOP CALCULATION (VOLATILITY BASED)
    # -------------------------
    stop_type = "volatility"
    atr_based = True

    stop_distance = _calculate_stop_distance(volatility, avg_range)

    # estimación simple de pérdida
    estimated_loss = final_size * max_risk_pct

    # -------------------------
    # RISK PROFILE
    # -------------------------
    risk_profile = _map_risk_profile(aggression_level)

    # -------------------------
    # BUILD OUTPUT
    # -------------------------
    return _build_output(
        valid=True,
        position_size=final_size,
        size_multiplier=size_multiplier,
        max_risk_pct=max_risk_pct,
        estimated_loss=estimated_loss,
        stop_type=stop_type,
        stop_distance=stop_distance,
        atr_based=atr_based,
        mode=mode,
        priority=priority,
        risk_profile=risk_profile,
        regime=regime_name,
        volatility=volatility,
        timestamp=timestamp,
        reasons=_build_reasons(confirmation, volatility)
    )


# =========================================================
# HELPERS
# =========================================================

def _base_position_size(aggression_level):
    if aggression_level == "high":
        return 1.0
    elif aggression_level == "medium":
        return 0.6
    else:
        return 0.3


def _calculate_stop_distance(volatility, avg_range):
    if volatility == "high":
        return avg_range * 1.5
    elif volatility == "medium":
        return avg_range * 1.0
    else:
        return avg_range * 0.7


def _map_risk_profile(aggression_level):
    if aggression_level == "high":
        return "aggressive"
    elif aggression_level == "medium":
        return "balanced"
    else:
        return "conservative"


def _build_reasons(confirmation, volatility):
    reasons = []

    if confirmation["signal_state"] == "weak":
        reasons.append("reduced confidence → smaller size")

    if confirmation["execution"]["mode"] == "passive":
        reasons.append("passive execution → conservative sizing")

    if volatility == "high":
        reasons.append("high volatility → wider stop")

    return reasons


# =========================================================
# OUTPUT BUILDER
# =========================================================

def _build_output(
    valid,
    position_size,
    size_multiplier,
    max_risk_pct,
    estimated_loss,
    stop_type,
    stop_distance,
    atr_based,
    mode,
    priority,
    risk_profile,
    regime,
    volatility,
    timestamp,
    reasons
):
    return {
        "valid": valid,

        "position": {
            "size": position_size,
            "size_multiplier": size_multiplier
        },

        "risk_limits": {
            "max_risk_pct": max_risk_pct,
            "estimated_loss": estimated_loss
        },

        "protection": {
            "stop_loss_type": stop_type,
            "stop_distance": stop_distance,
            "atr_based": atr_based
        },

        "execution_profile": {
            "mode": mode,
            "priority": priority,
            "risk_profile": risk_profile
        },

        "context": {
            "regime": regime,
            "volatility": volatility,
            "timestamp": timestamp
        },

        "reasons": reasons
    }

