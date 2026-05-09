def build_strategy(data):
    signal = data["signal"]
    confirmation = data["confirmation"]
    features = data["features"]
    regime = data["regime"]

    # -------------------------
    # CONTEXT
    # -------------------------
    permission = confirmation["execution"]["permission"]
    mode = confirmation["execution"]["mode"]
    priority = confirmation["execution"]["priority"]

    regime_name = regime["market_regime"].lower()
    signal_type = signal["type"].lower()
    direction = signal.get("bias", "undefined").lower()

    timestamp = confirmation["meta"].get("timestamp", 0)

    # -------------------------
    # HARD BLOCK
    # -------------------------
    if permission == "blocked":
        return _build_output(
            valid=False,
            strategy=_blocked_strategy(),
            execution_profile=_build_execution_profile(mode, priority),
            context=_build_context(regime_name, signal_type, timestamp),
            reasons=["blocked by confirmation layer"]
        )

    strategy = None
    is_weak_trend = regime_name == "weak_trend"

    # =====================================================
    # RANGE REGIME
    # =====================================================
    if regime_name == "range":

        if signal_type == "micro_range":
            strategy = {
                "entry_type": "limit",
                "entry_logic": "mean_reversion",
                "entry_zone": "extreme",
                "confirmation": False,
                "timeframe_alignment": False,
                "aggressiveness": "low",
                "direction": direction
            }

    # =====================================================
    # TREND + WEAK_TREND
    # =====================================================
    elif regime_name in ["trend", "weak_trend"]:

        base_entry = "market" if mode == "aggressive" else "limit"
        tf_align = not is_weak_trend

        # -------------------------
        # CONTINUATION / PULLBACK
        # -------------------------
        if signal_type in ["continuation", "pullback"]:

            strategy = {
                "entry_type": base_entry,
                "entry_logic": "trend_continuation",
                "entry_zone": "pullback",
                "confirmation": True,
                "timeframe_alignment": tf_align,
                "aggressiveness": (
                    "high"
                    if mode == "aggressive"
                    else "medium"
                ),
                "direction": direction
            }

        # -------------------------
        # BREAKOUT
        # -------------------------
        elif signal_type == "breakout":

            strategy = {
                "entry_type": "market",
                "entry_logic": "breakout",
                "entry_zone": "structure_break",
                "confirmation": True,
                "timeframe_alignment": tf_align,
                "aggressiveness": "high",
                "direction": direction
            }

        # =====================================================
        # 🔥 NUEVO:
        # MICRO RANGE EN WEAK TREND
        # =====================================================
        elif signal_type == "micro_range":

            if direction == "long":

                strategy = {
                    "entry_type": "limit",
                    "entry_logic": "pullback_reversion",
                    "entry_zone": "local_support",
                    "confirmation": True,
                    "timeframe_alignment": tf_align,
                    "aggressiveness": "medium",
                    "direction": "long"
                }

            elif direction == "short":

                strategy = {
                    "entry_type": "limit",
                    "entry_logic": "pullback_reversion",
                    "entry_zone": "local_resistance",
                    "confirmation": True,
                    "timeframe_alignment": tf_align,
                    "aggressiveness": "medium",
                    "direction": "short"
                }

    # -------------------------
    # FALLBACK
    # -------------------------
    if strategy is None:
        return _build_output(
            valid=False,
            strategy=_fallback_strategy(signal),
            execution_profile=_build_execution_profile(mode, priority),
            context=_build_context(regime_name, signal_type, timestamp),
            reasons=[
                f"no deterministic mapping found for "
                f"{signal_type}/{direction}/{regime_name}"
            ]
        )

    # -------------------------
    # EXECUTION PROFILE
    # -------------------------
    execution_profile = _build_execution_profile(
        mode,
        priority
    )

    # -------------------------
    # FINAL OUTPUT
    # -------------------------
    return _build_output(
        valid=True,
        strategy=strategy,
        execution_profile=execution_profile,
        context=_build_context(
            regime_name,
            signal_type,
            timestamp
        ),
        reasons=_build_reasons(strategy)
    )


# =====================================================
# STRATEGY BUILDERS
# =====================================================

def _blocked_strategy():
    return {
        "entry_type": "none",
        "entry_logic": "blocked",
        "entry_zone": "none",
        "confirmation": False,
        "timeframe_alignment": False,
        "aggressiveness": "undefined",
        "direction": "undefined"
    }


def _fallback_strategy(signal):
    return {
        "entry_type": "none",
        "entry_logic": "none",
        "entry_zone": "none",
        "confirmation": False,
        "timeframe_alignment": False,
        "aggressiveness": "undefined",
        "direction": signal.get("bias", "undefined")
    }


# =====================================================
# EXECUTION PROFILE
# =====================================================

def _build_execution_profile(mode, priority):
    return {
        "mode": mode,
        "priority": priority
    }


# =====================================================
# CONTEXT
# =====================================================

def _build_context(regime, signal_type, timestamp):
    return {
        "regime": regime,
        "signal_type": signal_type,
        "timestamp": timestamp
    }


# =====================================================
# OUTPUT
# =====================================================

def _build_output(
    valid,
    strategy,
    execution_profile,
    context,
    reasons
):
    return {
        "valid": valid,
        "strategy": strategy,
        "execution_profile": execution_profile,
        "context": context,
        "reasons": reasons
    }


# =====================================================
# REASONS
# =====================================================

def _build_reasons(strategy):
    return [
        f"entry_type={strategy['entry_type']}",
        f"entry_logic={strategy['entry_logic']}",
        f"entry_zone={strategy['entry_zone']}",
        f"direction={strategy['direction']}",
        f"aggressiveness={strategy['aggressiveness']}"
    ]