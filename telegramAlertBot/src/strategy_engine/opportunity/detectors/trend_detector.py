

from ..base_detector import BaseDetector


class TrendDetector(BaseDetector):
    name = "trend"

    def detect(self, features, market):
        trend = features.get("trend", {})

        if not trend.get("is_trending"):
            return {"detected": False}

        bias = trend.get("bias")

        return {
            "detected": True,
            "confidence": 0.75,
            "side": bias,
            "reason": f"Trend {trend.get('trend_direction')}"
        }

