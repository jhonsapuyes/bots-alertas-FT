

class TradePlanner:
    """
    Convierte la decisión del pipeline en un plan de ejecución.
    NO decide mercado.
    """

    def plan(self, features: dict, decision: dict, price: float = None) -> dict:

        volatility = features.get("volatility", {})
        avg_range = volatility.get("avg_range", 500)
        vol = volatility.get("volatility_level")

        action = decision.get("bias") or decision.get("action")
        confidence = decision.get("confidence", 0)
        size = decision.get("position_size", 0.5)
        execution_mode = decision.get("execution_mode", "reduced")

        # ----------------------------
        # MULTIPLICADOR VOLATILIDAD
        # ----------------------------
        if vol == "high":
            multiplier = 1.5
        elif vol == "low":
            multiplier = 0.8
        else:
            multiplier = 1.0

        move = avg_range * multiplier

        # ----------------------------
        # NO TRADE
        # ----------------------------
        if action == "NO_TRADE" or confidence < 0.5:
            return {
                "status": "no_trade",
                "reason": "low_confidence_or_blocked"
            }

        # ----------------------------
        # LONG (ejecución pura)
        # ----------------------------
        if action == "long" or action == "LONG":

            return {
                "side": "LONG",
                "execution_mode": execution_mode,
                "position_size": size,
                "entry_zone": [price - move * 0.2, price + move * 0.1],
                "stop_loss": price - move * 0.6,
                "take_profit": {
                    "tp1": price + move * 0.6,
                    "tp2": price + move * 1.2
                },
                "confidence": confidence
            }

        # ----------------------------
        # SHORT (ejecución pura)
        # ----------------------------
        if action == "short" or action == "SHORT":

            return {
                "side": "SHORT",
                "execution_mode": execution_mode,
                "position_size": size,
                "entry_zone": [price + move * 0.1, price + move * 0.2],
                "stop_loss": price + move * 0.6,
                "take_profit": {
                    "tp1": price - move * 0.6,
                    "tp2": price - move * 1.2
                },
                "confidence": confidence
            }

        return {
            "status": "invalid_action",
            "action": action
        }
    
