

from ..base_detector import BaseDetector


class LiquidityGrabDetector(BaseDetector):
    name = "liquidity_grab"

    def detect(self, features, market):
        vol = features.get("volatility", {})

        if vol.get("volatility_level") == "high":
            return {
                "detected": True,
                "confidence": 0.65,
                "side": None,
                "reason": "Possible liquidity sweep (high volatility spike)"
            }

        return {"detected": False}

