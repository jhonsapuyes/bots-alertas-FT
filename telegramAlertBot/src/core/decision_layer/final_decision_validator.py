

class FinalDecisionValidator:
    """
    🧠 Última capa de seguridad del sistema
    Evita decisiones peligrosas aunque el arbitrator diga BUY/SELL
    """

    def run(self, features: dict, opportunities: dict, decision: dict, regime_context: dict) -> dict:

        trend = features.get("trend", {})
        momentum = features.get("momentum", {})
        volatility = features.get("volatility", {})

        bias = decision.get("bias")
        confidence = decision.get("confidence", 0)
        regime = decision.get("regime")

        rsi = momentum.get("rsi", 50)
        vol = volatility.get("volatility_level", "medium")
        std = volatility.get("std_dev", 0)

        # -----------------------------
        # 🔴 1. HIGH VOLATILITY OVERRIDE
        # -----------------------------
        if vol == "high" and confidence < 0.8:
            return self._block(decision, "high_vol_low_confidence")

        # -----------------------------
        # 🔴 2. CONTRADICTION FILTER
        # -----------------------------
        if bias == "long" and momentum.get("momentum_state") == "bearish":
            return self._block(decision, "trend_momentum_conflict")

        if bias == "short" and momentum.get("momentum_state") == "bullish":
            return self._block(decision, "trend_momentum_conflict")

        # -----------------------------
        # 🔴 3. RSI EXTREME OVERRIDE
        # -----------------------------
        if rsi > 75 and bias == "long":
            return self._block(decision, "overbought_long_risk")

        if rsi < 30 and bias == "short":
            return self._block(decision, "oversold_short_risk")

        # -----------------------------
        # 🔴 4. BREAKOUT FAKE CHECK (VOLATILITY + RANGE RISK)
        # -----------------------------
        if regime == "range_market" and bias in ["long", "short"] and vol == "high":
            return self._block(decision, "fake_breakout_risk")

        # -----------------------------
        # ✅ APPROVED DECISION
        # -----------------------------
        decision["validated"] = True
        decision["validation_status"] = "approved"
        decision["risk_flag"] = "low" if confidence > 0.75 else "medium"

        return decision

    # -----------------------------
    # BLOCKED DECISION
    # -----------------------------
    def _block(self, decision: dict, reason: str) -> dict:

        return {
            **decision,
            "validated": False,
            "validation_status": "blocked",
            "block_reason": reason,
            "bias": "wait",
            "confidence": 0
        }

