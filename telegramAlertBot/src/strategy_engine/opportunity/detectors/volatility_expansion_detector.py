

from ..base_detector import BaseDetector


class VolatilityExpansionDetector(BaseDetector):
    name = "volatility_expansion"

    def detect(self, features, market):
        vol = features.get("volatility", {})

        if vol.get("volatility_level") == "high":
            return {
                "detected": True,
                "confidence": 0.7,
                "side": None,
                "reason": "Volatility expansion"
            }

        return {"detected": False}

