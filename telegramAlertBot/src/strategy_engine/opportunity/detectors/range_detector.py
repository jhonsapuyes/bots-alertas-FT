

from ...strategy_engine.opportunity.base_detector import BaseDetector


class RangeDetector(BaseDetector):
    name = "range"

    def detect(self, features, market):
        vol = features.get("volatility", {})

        if vol.get("volatility_level") == "low":
            return {
                "detected": True,
                "confidence": 0.8,
                "side": None,
                "reason": "Market in range (low volatility)"
            }

        return {"detected": False}

