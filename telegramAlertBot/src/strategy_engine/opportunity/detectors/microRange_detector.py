

from ..base_detector import BaseDetector


class MicroRangeDetector(BaseDetector):
    name = "micro_range"

    def detect(self, features, market):
        vol = features.get("volatility", {})

        if vol.get("avg_range", 0) < 5:
            return {
                "detected": True,
                "confidence": 0.7,
                "side": None,
                "reason": "Micro range compression"
            }

        return {"detected": False}

