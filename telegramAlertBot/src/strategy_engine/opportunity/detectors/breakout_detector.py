

from ..base_detector import BaseDetector


class BreakoutDetector(BaseDetector):
    name = "breakout"

    def detect(self, features, market):
        vol = features.get("volatility", {})
        trend = features.get("trend", {})

        if vol.get("volatility_level") == "high" and trend.get("is_trending"):
            return {
                "detected": True,
                "confidence": 0.8,
                "side": trend.get("bias"),
                "reason": "High volatility breakout setup"
            }

        return {"detected": False}

