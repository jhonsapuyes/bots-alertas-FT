from core.decision_layer.market_regime_controller import MarketRegimeController
from core.decision_layer.conflict_resolver import ConflictResolver
from core.decision_layer.final_decision_validator import FinalDecisionValidator
from core.decision_layer.risk_scaler import RiskScaler
from core.decision_layer.adaptive_execution_engine import AdaptiveExecutionEngine


class SignalArbitrator:

    def __init__(self):
        self.regime_controller = MarketRegimeController()
        self.conflict_resolver = ConflictResolver()

        # 🔥 NUEVO SISTEMA UNIFICADO (SIN ROMPER EL ANTIGUO)
        self.execution_engine = AdaptiveExecutionEngine()

        # ⚠️ aún se mantiene por compatibilidad (no lo usamos directamente)
        self.validator = FinalDecisionValidator()
        self.risk_scaler = RiskScaler()

    def run(self, engine_output: dict) -> dict:

        features = engine_output.get("features", {})
        filters = engine_output.get("filters", {})
        opportunities = engine_output.get("opportunities", {})

        signals = opportunities.get("signals", [])

        # 🧠 1. VALIDACIÓN BASE
        if not filters or not filters.get("valid", False):
            return self._empty("filters_blocked")

        if not signals:
            return self._empty("no_signals")

        # 🧠 2. REGIME CONTROLLER
        regime_context = self.regime_controller.run(features, opportunities)

        regime = regime_context.get("regime", self._detect_regime(features))
        preferred_bias = regime_context.get("preferred_bias", None)

        # 🧠 3. SCORING BASE
        evaluated = self._evaluate_signals(signals, features, regime)

        # 🧠 4. CONFLICT RESOLVER
        evaluated = self.conflict_resolver.run(evaluated, features, regime)

        evaluated.sort(key=lambda x: x["score"], reverse=True)

        best = evaluated[0]
        rejected = evaluated[1:]

        # 🧠 5. BIAS FINAL
        final_bias = best.get("side")

        if preferred_bias == "mean_reversion" and best["type"] in ["trend", "breakout"]:
            final_bias = "wait"

        if preferred_bias == "trend" and regime == "range_market":
            final_bias = "wait"

        # 🧠 6. DECISION BASE
        decision = {
            "regime": regime,
            "bias": final_bias,
            "active_signal": best["type"],
            "confidence": round(best["score"], 3),
            "reason": best.get("reason", ""),
            "conflicts_resolved": [s["type"] for s in rejected],
            "risk_mode": regime_context.get("risk_mode", "normal"),
            "conflict_level": regime_context.get("conflict_level", "low")
        }

        # 🔥 7. ADAPTIVE EXECUTION ENGINE (NUEVA VERDAD ÚNICA)
        final_decision = self.execution_engine.run(
            features=features,
            opportunities=opportunities,
            decision=decision,
            regime_context=regime_context
        )

        # 🧠 8. OUTPUT FINAL LIMPIO (SIN DUPLICACIÓN)
        return final_decision

    # -----------------------------
    # REGIME LOCAL (FALLBACK)
    # -----------------------------
    def _detect_regime(self, features: dict) -> str:

        trend = features.get("trend", {}).get("trend_strength", "")
        momentum = features.get("momentum", {}).get("momentum_state", "")

        if momentum in ["overbought", "oversold"]:
            return "mean_reversion"

        if trend == "strong":
            return "trend_following"

        if trend == "weak":
            return "range"

        return "uncertain"

    # -----------------------------
    # SCORING BASE
    # -----------------------------
    def _evaluate_signals(self, signals, features, regime):

        evaluated = []

        momentum_state = features.get("momentum", {}).get("momentum_state")

        for s in signals:

            score = s.get("confidence", 0)

            if regime == "mean_reversion":
                if s["type"] in ["trend", "breakout"] and momentum_state == "overbought":
                    score -= 0.25

            if regime == "trend_following":
                if s["type"] in ["mean_reversion", "reversal"]:
                    score -= 0.2

            if s.get("side") == "long" and momentum_state == "overbought":
                score -= 0.15

            if s.get("side") == "short" and momentum_state == "oversold":
                score -= 0.15

            evaluated.append({
                **s,
                "score": round(score, 4)
            })

        return evaluated

    # -----------------------------
    # OUTPUT LIMPIO
    # -----------------------------
    def _empty(self, reason):
        return {
            "regime": "uncertain",
            "bias": None,
            "active_signal": None,
            "confidence": 0,
            "reason": reason,
            "conflicts_resolved": [],
            "position_size": 0,
            "risk_mode": "blocked"
        }
    
