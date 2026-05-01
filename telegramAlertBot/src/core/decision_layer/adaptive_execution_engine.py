

# core/decision_layer/adaptive_execution_engine.py


class AdaptiveExecutionEngine:
    """
    🧠 Combina validación + risk scaling en una sola capa adaptativa

    NO bloquea trades agresivamente
    SOLO ajusta exposición según riesgo del mercado
    """

    def run(self, features: dict, opportunities: dict, decision: dict, regime_context: dict) -> dict:

        regime = regime_context.get("regime", "uncertain")
        conflict_level = regime_context.get("conflict_level", "low")
        volatility = features.get("volatility", {}).get("volatility_level", "medium")

        confidence = decision.get("confidence", 0)
        bias = decision.get("bias")

        # -----------------------------
        # 🧠 1. BASE VALIDATION SCORE
        # -----------------------------
        validation_score = confidence

        if conflict_level == "high":
            validation_score -= 0.25

        if regime in ["range_market", "transition_market"]:
            validation_score -= 0.15

        if volatility == "high":
            validation_score -= 0.10

        # -----------------------------
        # 🧠 2. DECISION STATE
        # -----------------------------
        if validation_score < 0.25:
            return {
                **decision,
                "validated": False,
                "execution_mode": "blocked",
                "position_size": 0.0,
                "risk_mode": "none",
                "validation_score": round(validation_score, 3),
                "reason": "low_confidence_risk_adjusted"
            }

        # -----------------------------
        # 🧠 3. ADAPTIVE RISK SCALING
        # -----------------------------
        base_size = 1.0

        # reducción por conflicto
        if conflict_level == "high":
            base_size *= 0.5

        # reducción por volatilidad
        if volatility == "high":
            base_size *= 0.6

        # ajuste por régimen
        if regime == "trend_following":
            base_size *= 1.0

        elif regime == "mean_reversion":
            base_size *= 0.8

        elif regime == "range_market":
            base_size *= 0.5

        # ajuste por confianza
        base_size *= confidence

        # -----------------------------
        # 🧠 4. FINAL DECISION
        # -----------------------------
        execution_mode = "full"

        if base_size < 0.3:
            execution_mode = "micro"
        elif base_size < 0.6:
            execution_mode = "reduced"

        return {
            **decision,
            "validated": True,
            "execution_mode": execution_mode,
            "position_size": round(base_size, 3),
            "risk_mode": "adaptive",
            "validation_score": round(validation_score, 3)
        }

