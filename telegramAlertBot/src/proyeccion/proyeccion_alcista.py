

from statistics import mean


import statistics
import math


def proyeccion_alcista(candles,feature_data,market_analysis,trade_plan):
    """
    Estimador probabilístico de tiempo hacia TP1/TP2/TP3
    usando:
    
    - candles reales
    - velocidad real
    - drift
    - volatilidad realizada
    - efficiency ratio
    - contexto de mercado
    """

    # ==========================================
    # VALIDACION
    # ==========================================

    if len(candles) < 3:
        return {
            "valid": False,
            "reason": "not_enough_candles"
        }

    # ==========================================
    # EXTRAER CLOSES
    # ==========================================

    closes = [c["close"] for c in candles]

    # ==========================================
    # RETURNS
    # ==========================================

    returns = []

    for i in range(1, len(closes)):

        prev_close = closes[i - 1]
        curr_close = closes[i]

        r = (
            curr_close - prev_close
        ) / prev_close

        returns.append(r)

    # ==========================================
    # DRIFT
    # ==========================================

    drift = sum(returns) / len(returns)

    # ==========================================
    # VOLATILIDAD REALIZADA
    # ==========================================

    realized_volatility = (
        statistics.stdev(returns)
        if len(returns) > 1
        else 0
    )

    # ==========================================
    # VELOCIDAD REAL
    # ==========================================

    candle_progress = []

    for candle in candles:

        movement = abs(
            candle["close"] - candle["open"]
        )

        candle_progress.append(movement)

    real_velocity = (
        sum(candle_progress)
        / len(candle_progress)
    )

    # ==========================================
    # EFFICIENCY RATIO (KAUFMAN)
    # ==========================================

    net_movement = abs(
        closes[-1] - closes[0]
    )

    total_movement = 0

    for i in range(1, len(closes)):
        total_movement += abs(
            closes[i] - closes[i - 1]
        )

    efficiency_ratio = (
        net_movement / total_movement
        if total_movement > 0
        else 0
    )

    # ==========================================
    # FEATURE CONTEXT
    # ==========================================

    trend_strength = (
        feature_data["features"]["trend"]["trend_strength"]
    )

    momentum_state = (
        feature_data["features"]["momentum"]["momentum_state"]
    )

    volatility_level = (
        feature_data["features"]["volatility"]["volatility_level"]
    )

    regime = (
        market_analysis["regime"]["market_regime"]
    )

    # ==========================================
    # SCORES
    # ==========================================

    trend_map = {
        "weak": 0.4,
        "moderate": 0.7,
        "strong": 1.0
    }

    momentum_map = {
        "weak": 0.3,
        "neutral": 0.5,
        "moderate": 0.75,
        "strong": 1.0
    }

    volatility_map = {
        "low": 0.5,
        "medium": 0.7,
        "normal": 0.7,
        "high": 1.0
    }

    trend_score = (
        trend_map.get(trend_strength, 0.4)
    )

    momentum_score = (
        momentum_map.get(momentum_state, 0.5)
    )

    volatility_score = (
        volatility_map.get(volatility_level, 0.7)
    )

    # ==========================================
    # EXPECTED VELOCITY
    # ==========================================

    expected_velocity = (
        real_velocity
        * efficiency_ratio
        * trend_score
        * momentum_score
        * volatility_score
    )

    # evitar cero
    expected_velocity = max(
        expected_velocity,
        0.1
    )

    # ==========================================
    # FRICTION FACTOR
    # ==========================================

    friction_factor = 1.0

    if regime == "weak_trend":
        friction_factor = 1.5

    elif regime == "range":
        friction_factor = 2.0

    elif regime == "strong_trend":
        friction_factor = 0.8

    # ==========================================
    # TRADE DATA
    # ==========================================

    entry_price = (
        trade_plan["trade"]["entry"]["price"]
    )

    stop_loss = (
        trade_plan["trade"]["stop_loss"]["price"]
    )

    tps = (
        trade_plan["trade"]["take_profit"]
    )

    # ==========================================
    # TARGET ESTIMATION
    # ==========================================

    targets = {}

    for tp_name, tp_price in tps.items():

        distance = abs(
            tp_price - entry_price
        )

        candles_needed = (
            distance / expected_velocity
        ) * friction_factor

        # 1h timeframe
        estimated_hours = candles_needed

        # ======================================
        # CONFIDENCE
        # ======================================

        confidence_score = (
            efficiency_ratio
            * trend_score
            * momentum_score
        )

        if confidence_score >= 0.65:
            confidence = "high"

        elif confidence_score >= 0.4:
            confidence = "medium"

        else:
            confidence = "low"

        # ======================================
        # TP HIT PROBABILITY
        # ======================================

        sl_distance = abs(
            entry_price - stop_loss
        )

        rr = (
            distance / sl_distance
            if sl_distance > 0
            else 0
        )

        base_probability = (
            confidence_score
            * (1 / (1 + rr * 0.6))
        )

        base_probability = max(
            0.05,
            min(base_probability, 0.95)
        )

        # ======================================
        # STORE
        # ======================================

        targets[tp_name] = {

            "price": round(tp_price, 2),

            "distance": round(distance, 2),

            "estimated_candles": round(
                candles_needed,
                2
            ),

            "estimated_hours": round(
                estimated_hours,
                2
            ),

            "confidence": confidence,

            "hit_probability": round(
                base_probability,
                2
            )
        }

    # ==========================================
    # OUTPUT
    # ==========================================

    return {

        "valid": True,

        "time_estimation": {

            "model": "dynamic_velocity_model",

            "market_dynamics": {

                "real_velocity": round(
                    real_velocity,
                    4
                ),

                "drift": round(
                    drift,
                    6
                ),

                "realized_volatility": round(
                    realized_volatility,
                    6
                ),

                "efficiency_ratio": round(
                    efficiency_ratio,
                    4
                ),

                "trend_score": trend_score,

                "momentum_score": momentum_score,

                "volatility_score": volatility_score,

                "expected_velocity": round(
                    expected_velocity,
                    4
                ),

                "friction_factor": friction_factor
            },

            "targets": targets,

            "meta": {

                "regime": regime,

                "trend_strength": trend_strength,

                "momentum": momentum_state,

                "volatility": volatility_level,

                "timeframe": "1h"
            }
        }
    }

