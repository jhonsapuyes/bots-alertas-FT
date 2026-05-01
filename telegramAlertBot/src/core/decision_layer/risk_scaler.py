

class RiskScaler:
    """
    🧠 Ajusta el tamaño de posición según calidad del trade
    NO decide entradas, solo EXPOSICIÓN
    """

    def run(self, features: dict, decision: dict, regime_context: dict) -> dict:

        trend = features.get("trend", {})
        momentum = features.get("momentum", {})
        volatility = features.get("volatility", {})

        base_confidence = decision.get("confidence", 0)
        bias = decision.get("bias")
        conflict_level = regime_context.get("conflict_level", "low")
        preferred_bias = regime_context.get("preferred_bias", "neutral")

        # 🔥 1. BASE SIZE
        size = 1.0

        # ⚠️ 2. REDUCCIÓN POR CONFLICTO
        if conflict_level == "high":
            size *= 0.4

        elif conflict_level == "medium":
            size *= 0.7

        # 📉 3. VOLATILIDAD
        vol = volatility.get("volatility_level", "medium")

        if vol == "high":
            size *= 0.5

        elif vol == "low":
            size *= 1.1

        # 🧠 4. CALIDAD DE SEÑAL
        if base_confidence >= 0.8:
            size *= 1.0

        elif base_confidence >= 0.6:
            size *= 0.7

        else:
            size *= 0.4

        # ⚖️ 5. COHERENCIA CON REGIMEN
        if preferred_bias == "trend" and bias == "long":
            size *= 1.1

        if preferred_bias == "mean_reversion" and bias == "wait":
            size *= 0.3

        # 🔒 6. CAP LIMITS
        size = max(0.1, min(size, 1.0))

        return {
            "position_size_multiplier": round(size, 2),
            "risk_mode": "high" if size < 0.4 else "normal",
            "reason": "risk adjusted by conflict + volatility + confidence"
        }

