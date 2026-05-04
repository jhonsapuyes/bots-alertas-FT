

from ...strategy_engine.opportunity.base_detector import BaseDetector


class ExhaustionDetector(BaseDetector):
    name = "exhaustion"

    def detect(self, features, market):
        mom = features.get("momentum", {})

        if mom.get("momentum_strength") == "strong" and mom.get("continuation") is False:
            return {
                "detected": True,
                "confidence": 0.6,
                "side": None,
                "reason": "Momentum exhaustion detected"
            }

        return {"detected": False}

