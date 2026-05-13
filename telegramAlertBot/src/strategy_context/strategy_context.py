

def strategy_context1(features, market_analysis, adaptive_context):

    trend = features["trend"]
    momentum = features["momentum"]

    regime = market_analysis["regime"]
    confirmation = market_analysis["confirmation"]

    signals = market_analysis.get(
        "signal",
        []
    )

    # =========================================================
    # NORMALIZATION
    # =========================================================

    trend_direction = str(
        trend.get("trend_direction", "")
    ).strip().lower()

    structure_state = str(
        trend.get("structure_state", "")
    ).strip().lower()

    momentum_strength = str(
        momentum.get("momentum_strength", "")
    ).strip().lower()

    market_regime = str(
        regime.get("market_regime", "")
    ).strip().lower()

    allow_anticipation = adaptive_context.get(
        "allow_anticipation",
        False
    )

    strategy_mode = str(
        adaptive_context.get(
            "strategy_mode",
            "neutral"
        )
    ).strip().lower()

    risk_modifier = adaptive_context.get(
        "risk_modifier",
        1.0
    )

    # =========================================================
    # RESPONSE
    # =========================================================

    response = {
        "valid": False,

        "strategy": {
            "entry_type": None,
            "entry_logic": None,
            "entry_zone": None,
            "confirmation": False,
            "timeframe_alignment": False,
            "aggressiveness": "low",
            "direction": None
        },

        "execution_profile": {
            "mode": "skip",
            "priority": "low"
        },

        "risk": {
            "modifier": risk_modifier,
            "size": 0.0
        },

        "context": {
            "regime": market_regime,
            "signal_type": None,
            "timestamp": 0
        },

        "reasons": []
    }

    # =========================================================
    # SIGNAL EXTRACTION
    # =========================================================

    signal_type = None
    signal_bias = None

    if len(signals) > 0:

        signal = signals[0]

        signal_type = signal.get(
            "type",
            None
        )

        signal_bias = signal.get(
            "bias",
            None
        )

        response["context"]["signal_type"] = (
            signal_type
        )

    # =========================================================
    # EARLY TREND FOLLOW
    # =========================================================

    if strategy_mode == "early_trend_follow":

        bullish_structure = (
            trend_direction == "bullish"
            and structure_state in [
                "bullish",
                "bullish_recovery"
            ]
        )

        momentum_valid = (
            momentum_strength in [
                "moderate",
                "strong"
            ]
        )

        if (
            bullish_structure
            and momentum_valid
            and allow_anticipation
        ):

            response["valid"] = True

            response["strategy"] = {
                "entry_type": "limit",
                "entry_logic": "mean_reversion",
                "entry_zone": "extreme",
                "confirmation": confirmation.get(
                    "confirmed",
                    False
                ),
                "timeframe_alignment": False,
                "aggressiveness": "low",
                "direction": signal_bias
            }

            response["execution_profile"] = {
                "mode": "passive",
                "priority": "low"
            }

            response["risk"]["size"] = (
                0.5 * risk_modifier
            )

            response["reasons"].append(
                "entry_type=limit"
            )

            response["reasons"].append(
                "entry_logic=mean_reversion"
            )

            response["reasons"].append(
                "entry_zone=extreme"
            )

            response["reasons"].append(
                f"direction={signal_bias}"
            )

            response["reasons"].append(
                "aggressiveness=low"
            )

    # =========================================================
    # FALLBACK
    # =========================================================

    if response["valid"] is False:

        response["execution_profile"] = {
            "mode": "skip",
            "priority": "low"
        }

        response["reasons"].append(
            "no valid strategy context"
        )

    return response



def strategy_context(features, market_analysis, adaptive_context):

    market_analysis["confirmation"]["confirmed"]=True
    #print(market_analysis["confirmation"]["confirmed"])

    trend = features["trend"]
    momentum = features["momentum"]
    price = features.get("price", {})

    regime = market_analysis["regime"]
    confirmation = market_analysis["confirmation"]

    signals = market_analysis.get(
        "signal",
        []
    )

    # =========================================================
    # NORMALIZATION
    # =========================================================

    trend_direction = str(
        trend.get("trend_direction", "")
    ).strip().lower()

    structure_state = str(
        trend.get("structure_state", "")
    ).strip().lower()

    momentum_strength = str(
        momentum.get("momentum_strength", "")
    ).strip().lower()

    market_regime = str(
        regime.get("market_regime", "")
    ).strip().lower()

    allow_anticipation = adaptive_context.get(
        "allow_anticipation",
        False
    )

    risk_modifier = adaptive_context.get(
        "risk_modifier",
        1.0
    )

    # =========================================================
    # RESPONSE
    # =========================================================

    response = {
        "valid": False,

        "strategy": {
            "entry_type": None,
            "entry_logic": None,
            "entry_zone": None,
            "confirmation": False,
            "timeframe_alignment": False,
            "aggressiveness": "low",
            "direction": None
        },

        "execution_profile": {
            "mode": "skip",
            "priority": "low"
        },

        "risk": {
            "modifier": risk_modifier,
            "size": 0.0
        },

        "context": {
            "regime": market_regime,
            "signal_type": None,
            "timestamp": 0
        },

        "reasons": []
    }

    # =========================================================
    # SIGNAL EXTRACTION
    # =========================================================

    signal_type = None
    signal_bias = None

    if len(signals) > 0:

        signal = signals[0]

        signal_type = str(
            signal.get("type", "")
        ).strip().lower()

        signal_bias = str(
            signal.get("bias", "")
        ).strip().lower()

        response["context"]["signal_type"] = (
            signal_type
        )

    # =========================================================
    # AUTO STRATEGY RESOLVER
    # =========================================================

    strategy_mode = "neutral"

    # ---------------------------------
    # EARLY TREND FOLLOW
    # ---------------------------------

    bullish_structure = (
        trend_direction == "bullish"
        and structure_state in [
            "bullish",
            "bullish_recovery"
        ]
    )

    momentum_valid = (
        momentum_strength in [
            "moderate",
            "strong"
        ]
    )

    if (
        bullish_structure
        and momentum_valid
        and allow_anticipation
    ):

        strategy_mode = (
            "early_trend_follow"
        )

    # ---------------------------------
    # MICRO RANGE REVERSION
    # ---------------------------------

    elif (
        market_regime in [
            "weak_trend",
            "sideways"
        ]
        and signal_type == "micro_range"
    ):

        strategy_mode = (
            "micro_range_reversion"
        )

    # =========================================================
    # EARLY TREND FOLLOW
    # =========================================================

    if strategy_mode == "early_trend_follow":

        response["valid"] = True

        response["strategy"] = {
            "entry_type": "limit",
            "entry_logic": "mean_reversion",
            "entry_zone": "extreme",
            "confirmation": confirmation.get(
                "confirmed",
                False
            ),
            "timeframe_alignment": False,
            "aggressiveness": "low",
            "direction": signal_bias
        }

        response["execution_profile"] = {
            "mode": "passive",
            "priority": "low"
        }

        response["risk"]["size"] = (
            0.5 * risk_modifier
        )

        response["reasons"].append(
            "strategy=early_trend_follow"
        )

        response["reasons"].append(
            "entry_type=limit"
        )

        response["reasons"].append(
            "entry_logic=mean_reversion"
        )

        response["reasons"].append(
            "entry_zone=extreme"
        )

        response["reasons"].append(
            f"direction={signal_bias}"
        )

        response["reasons"].append(
            "aggressiveness=low"
        )

    # =========================================================
    # MICRO RANGE REVERSION
    # =========================================================

    elif strategy_mode == "micro_range_reversion":

        last_close = float(
            price.get("last_close", 0.0)
        )

        last_high = float(
            price.get("last_high", 0.0)
        )

        last_low = float(
            price.get("last_low", 0.0)
        )

        range_size = (
            last_high - last_low
        )

        range_position = 0.5

        if range_size > 0:

            range_position = (
                (last_close - last_low)
                / range_size
            )

        # ---------------------------------
        # DIRECTION FROM RANGE POSITION
        # ---------------------------------

        direction = "neutral"

        if range_position <= 0.35:

            direction = "long"

        elif range_position >= 0.65:

            direction = "short"

        if direction != "neutral":

            response["valid"] = True

            response["strategy"] = {
                "entry_type": "limit",
                "entry_logic": "mean_reversion",
                "entry_zone": "range_extreme",
                "confirmation": confirmation.get(
                    "confirmed",
                    False
                ),
                "timeframe_alignment": False,
                "aggressiveness": "low",
                "direction": direction
            }

            response["execution_profile"] = {
                "mode": "passive",
                "priority": "medium"
            }

            response["risk"]["size"] = (
                0.25 * risk_modifier
            )

            response["reasons"].append(
                "strategy=micro_range_reversion"
            )

            response["reasons"].append(
                "entry_type=limit"
            )

            response["reasons"].append(
                "entry_logic=mean_reversion"
            )

            response["reasons"].append(
                "entry_zone=range_extreme"
            )

            response["reasons"].append(
                f"direction={direction}"
            )

            response["reasons"].append(
                f"range_position={round(range_position, 2)}"
            )

            response["reasons"].append(
                "aggressiveness=low"
            )

    # =========================================================
    # FALLBACK
    # =========================================================

    if response["valid"] is False:

        response["execution_profile"] = {
            "mode": "skip",
            "priority": "low"
        }

        response["reasons"].append(
            "no valid strategy context"
        )

    return response




