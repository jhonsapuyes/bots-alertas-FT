

from ..base_detector import BaseDetector


class PullbackDetector(BaseDetector):
    name = "pullback"

    def detect(self, features, market):
        trend = features.get("trend", {})
        momentum = features.get("momentum", {})

        if trend.get("is_trending") and momentum.get("entry_timing") in ["good_for_long", "good_for_short"]:
            return {
                "detected": True,
                "confidence": 0.7,
                "side": trend.get("bias"),
                "reason": "Pullback in trend"
            }

        return {"detected": False}

