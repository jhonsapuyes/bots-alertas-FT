

# core/decision_layer/market_regime_controller.py

class MarketRegimeController:
    """
    🧠 Detecta el tipo de mercado + INFLUYE en decisiones (soft power)
    """

    def run(self, features: dict, opportunities: dict) -> dict:

        trend = features.get("trend", {})
        momentum = features.get("momentum", {})
        volatility = features.get("volatility", {})

        signals = opportunities.get("signals", [])

        is_trending = trend.get("is_trending", False)
        trend_strength = trend.get("trend_strength", "weak")
        rsi = momentum.get("rsi", 50)
        vol = volatility.get("volatility_level", "medium")
        std = volatility.get("std_dev", 0)

        # -----------------------------
        # 🧠 1. REGIME
        # -----------------------------
        if is_trending and rsi > 70:
            regime = "trend_exhaustion"
            preferred_bias = "mean_reversion"

        elif is_trending and rsi < 55:
            regime = "trend_following"
            preferred_bias = "trend"

        elif not is_trending:
            regime = "range_market"
            preferred_bias = "mean_reversion"

        else:
            regime = "transition_market"
            preferred_bias = "neutral"

        # -----------------------------
        # 🌊 2. MARKET PHASE
        # -----------------------------
        market_phase = "expansion" if (is_trending and trend_strength == "strong") else "contraction"

        # -----------------------------
        # ⚖️ 3. 🔥 SIGNAL WEIGHTS (LO IMPORTANTE)
        # -----------------------------
        signal_weights = {
            "trend": 1.0,
            "breakout": 1.0,
            "pullback": 1.0,
            "mean_reversion": 1.0,
            "reversal": 1.0
        }

        # 🧠 ajustes según régimen
        if regime == "trend_following":
            signal_weights["trend"] = 1.3
            signal_weights["breakout"] = 1.2
            signal_weights["mean_reversion"] = 0.7
            signal_weights["reversal"] = 0.8

        elif regime == "mean_reversion":
            signal_weights["reversal"] = 1.3
            signal_weights["mean_reversion"] = 1.2
            signal_weights["trend"] = 0.7
            signal_weights["breakout"] = 0.8

        elif regime == "range_market":
            signal_weights["pullback"] = 1.2
            signal_weights["reversal"] = 1.2
            signal_weights["breakout"] = 0.6

        # -----------------------------
        # ⚠️ 4. CONFLICTO (EXISTENTE)
        # -----------------------------
        sides = [s.get("side") for s in signals if s.get("side")]

        conflict_level = "low"
        if len(set(sides)) > 1:
            conflict_level = "high"

        # -----------------------------
        # 🔥 OUTPUT ÚTIL (NO DECORATIVO)
        # -----------------------------
        return {
            "regime": regime,
            "preferred_bias": preferred_bias,
            "market_phase": market_phase,
            "volatility_level": vol,
            "risk_mode": "high" if std > 0.006 else "normal",
            "conflict_level": conflict_level,

            # 🔥 ESTO ES LO QUE LO HACE ÚTIL REALMENTE
            "signal_weights": signal_weights
        }
     
