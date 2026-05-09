

# =====================================================
# TRADE PLANNER
# =====================================================

def build_trade_plan(data):

    # =====================================================
    # INPUTS
    # =====================================================

    features = data["features"]
    regime = data["regime"]
    signal = data["signal"]
    confirmation = data["confirmation"]
    strategy_data = data["strategy"]
    risk = data["risk"]

    # =====================================================
    # VALIDATIONS
    # =====================================================

    if not confirmation["confirmed"]:
        return _blocked_output(
            regime=regime,
            signal=signal,
            strategy_data=strategy_data,
            reason="trade not confirmed"
        )

    if not strategy_data["valid"]:
        return _blocked_output(
            regime=regime,
            signal=signal,
            strategy_data=strategy_data,
            reason="strategy invalid"
        )

    if not risk["valid"]:
        return _blocked_output(
            regime=regime,
            signal=signal,
            strategy_data=strategy_data,
            reason="risk validation failed"
        )

    # =====================================================
    # CORE CONTEXT
    # =====================================================

    strategy = strategy_data["strategy"]

    side = signal["bias"]

    entry_type = strategy["entry_type"]
    strategy_logic = strategy["entry_logic"]

    # =====================================================
    # MARKET DATA
    # =====================================================

    price = features["price"]

    last_close = price["last_close"]
    last_high = price["last_high"]
    last_low = price["last_low"]

    volatility = features["volatility"]

    avg_range = volatility["avg_range"]

    # =====================================================
    # ENTRY
    # =====================================================

    entry_price = round(last_close, 2)

    zone_buffer = avg_range * 0.15

    zone_low = round(entry_price - zone_buffer, 2)
    zone_high = round(entry_price + zone_buffer, 2)

    # =====================================================
    # STOP LOSS
    # =====================================================

    atr_multiple = 1.2

    stop_distance = avg_range * atr_multiple

    if side == "long":
        stop_price = round(
            entry_price - stop_distance,
            2
        )

    else:
        stop_price = round(
            entry_price + stop_distance,
            2
        )

    distance_pct = round(
        abs(entry_price - stop_price)
        / entry_price * 100,
        2
    )

    # =====================================================
    # TAKE PROFITS
    # =====================================================

    risk_distance = abs(
        entry_price - stop_price
    )

    if side == "long":

        tp1 = round(
            entry_price + risk_distance * 1.0,
            2
        )

        tp2 = round(
            entry_price + risk_distance * 1.8,
            2
        )

        tp3 = round(
            entry_price + risk_distance * 2.5,
            2
        )

    else:

        tp1 = round(
            entry_price - risk_distance * 1.0,
            2
        )

        tp2 = round(
            entry_price - risk_distance * 1.8,
            2
        )

        tp3 = round(
            entry_price - risk_distance * 2.5,
            2
        )

    # =====================================================
    # RISK / REWARD
    # =====================================================

    rr_1 = 1.0
    rr_2 = 1.8
    rr_3 = 2.5

    # =====================================================
    # POSITION
    # =====================================================

    position_data = risk["position"]
    risk_limits = risk["risk_limits"]

    size = position_data.get(
        "size_multiplier",
        0.0
    )

    risk_pct = risk_limits.get(
        "max_risk_pct",
        0.0
    )

    estimated_loss = risk_limits.get(
        "estimated_loss",
        None
    )

    leverage = _calculate_leverage(
        confidence=confirmation[
            "confidence_score"
        ],
        volatility=volatility[
            "volatility_level"
        ]
    )

    # =====================================================
    # EXECUTION
    # =====================================================

    execution_mode = confirmation[
        "execution"
    ]["mode"]

    execution_ready = True

    reduce_only = False

    time_in_force = (
        "IOC"
        if execution_mode == "aggressive"
        else "GTC"
    )

    slippage_tolerance = 0.1

    # =====================================================
    # FINAL OUTPUT
    # =====================================================

    return {

        # =================================================
        # VALIDATION
        # =================================================

        "valid": True,

        # =================================================
        # META
        # =================================================

        "meta": {
            "pipeline_stage": "TRADE_PLANNER",
            "version": "1.0",
            "generated_by": "strategy_v3"
        },

        # =================================================
        # TRADE
        # =================================================

        "trade": {

            # ---------------------------------------------
            # DIRECTION
            # ---------------------------------------------

            "side": side,

            # ---------------------------------------------
            # ENTRY
            # ---------------------------------------------

            "entry": {
                "type": entry_type,
                "price": entry_price,
                "zone_low": zone_low,
                "zone_high": zone_high
            },

            # ---------------------------------------------
            # STOP LOSS
            # ---------------------------------------------

            "stop_loss": {
                "price": stop_price,
                "distance_pct": distance_pct,
                "atr_multiple": atr_multiple
            },

            # ---------------------------------------------
            # TAKE PROFIT
            # ---------------------------------------------

            "take_profit": {
                "tp1": tp1,
                "tp2": tp2,
                "tp3": tp3
            },

            # ---------------------------------------------
            # RISK REWARD
            # ---------------------------------------------

            "risk_reward": {
                "tp1_rr": rr_1,
                "tp2_rr": rr_2,
                "tp3_rr": rr_3
            },

            # ---------------------------------------------
            # POSITION
            # ---------------------------------------------

            "position": {
                "size": size,
                "leverage": leverage
            },

            # ---------------------------------------------
            # RISK
            # ---------------------------------------------

            "risk": {
                "risk_pct": risk_pct,
                "max_loss": estimated_loss
            },

            # ---------------------------------------------
            # EXECUTION
            # ---------------------------------------------

            "execution": {
                "ready": execution_ready,
                "order_type": entry_type,
                "time_in_force": time_in_force,
                "reduce_only": reduce_only,
                "slippage_tolerance": (
                    slippage_tolerance
                )
            }
        },

        # =================================================
        # CONTEXT
        # =================================================

        "context": {
            "regime": regime[
                "market_regime"
            ],
            "signal_type": signal[
                "type"
            ],
            "strategy_logic": (
                strategy_logic
            )
        },

        # =================================================
        # REASONS
        # =================================================

        "reasons": _build_reasons(
            signal,
            regime,
            strategy_logic
        )
    }


# =====================================================
# BLOCKED OUTPUT
# =====================================================

def _blocked_output(
    regime,
    signal,
    strategy_data,
    reason
):

    return {

        "valid": False,

        "meta": {
            "pipeline_stage": "TRADE_PLANNER",
            "version": "1.0",
            "generated_by": "strategy_v3"
        },

        "trade": None,

        "context": {
            "regime": regime[
                "market_regime"
            ],

            "signal_type": signal[
                "type"
            ],

            "strategy_logic": (
                strategy_data
                .get("strategy", {})
                .get(
                    "entry_logic",
                    "none"
                )
            )
        },

        "reasons": [reason]
    }


# =====================================================
# LEVERAGE
# =====================================================

def _calculate_leverage(
    confidence,
    volatility
):

    leverage = 1

    if confidence >= 0.60:
        leverage += 1

    if volatility == "low":
        leverage += 1

    return leverage


# =====================================================
# REASONS
# =====================================================

def _build_reasons(
    signal,
    regime,
    strategy_logic
):

    reasons = []

    direction = signal.get("bias")

    if direction == "long":

        reasons.append(
            "bullish directional pressure"
        )

    elif direction == "short":

        reasons.append(
            "bearish directional pressure"
        )

    if strategy_logic == (
        "pullback_reversion"
    ):

        reasons.append(
            "pullback into local support/resistance"
        )

    if regime[
        "market_regime"
    ] == "weak_trend":

        reasons.append(
            "controlled weak trend environment"
        )

    reasons.append(
        "acceptable RR profile"
    )

    return reasons 