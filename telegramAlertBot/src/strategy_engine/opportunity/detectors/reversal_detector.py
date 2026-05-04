

from ...strategy_engine.opportunity.base_detector import BaseDetector


class ReversalDetector(BaseDetector):
    name = "reversal"

    def detect(self, features, market):
        trend = features.get("trend", {})
        mom = features.get("momentum", {})

        if trend.get("trend_direction") == "bullish" and mom.get("momentum_state") == "bearish":
            return {
                "detected": True,
                "confidence": 0.8,
                "side": "short",
                "reason": "Trend-momentum divergence reversal"
            }

        return {"detected": False}

