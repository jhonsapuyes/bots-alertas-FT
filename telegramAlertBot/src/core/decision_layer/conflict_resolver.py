

# core/decision_layer/conflict_resolver.py

class ConflictResolver:
    """
    🧠 RESUELVE CONFLICTOS ENTRE SEÑALES
    NO decide trades
    SOLO estabiliza lógica de mercado
    """

    def run(self, signals: list, features: dict, regime: str) -> list:

        resolved = []

        momentum_state = features.get("momentum", {}).get("momentum_state", "")
        trend_strength = features.get("trend", {}).get("trend_strength", "")

        for s in signals:

            score = s.get("confidence", 0)
            signal_type = s.get("type")
            side = s.get("side")

            # ----------------------------
            # 1. conflicto tendencia vs reversión
            # ----------------------------
            if regime == "mean_reversion":

                if signal_type in ["trend", "breakout"]:
                    score -= 0.25

            # ----------------------------
            # 2. conflicto trend-following
            # ----------------------------
            if regime == "trend_following":

                if signal_type in ["reversal", "mean_reversion"]:
                    score -= 0.2

            # ----------------------------
            # 3. debilidad de tendencia
            # ----------------------------
            if trend_strength == "weak" and signal_type == "trend":
                score -= 0.15

            # ----------------------------
            # 4. sobrecompra / sobreventa
            # ----------------------------
            if side == "long" and momentum_state == "overbought":
                score -= 0.15

            if side == "short" and momentum_state == "oversold":
                score -= 0.15

            # ----------------------------
            # 5. boost coherente
            # ----------------------------
            if regime == "trend_following" and signal_type == "trend":
                score += 0.1

            resolved.append({
                **s,
                "score": round(score, 4)
            })

        return resolved

