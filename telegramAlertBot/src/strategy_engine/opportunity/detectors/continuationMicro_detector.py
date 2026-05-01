

from ..base_detector import BaseDetector


class ContinuationMicroDetector(BaseDetector):
    name = "continuation_micro"

    def detect(self, features, market):
        trend = features.get("trend", {})
        vol = features.get("volatility", {})

        if trend.get("is_trending") and vol.get("volatility_level") == "low":
            return {
                "detected": True,
                "confidence": 0.7,
                "side": trend.get("bias"),
                "reason": "Micro continuation in trend"
            }

        return {"detected": False}

