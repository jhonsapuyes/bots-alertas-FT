

from ..base_detector import BaseDetector


class MomentumIgnitionDetector(BaseDetector):
    name = "momentum_ignition"

    def detect(self, features, market):
        mom = features.get("momentum", {})

        if mom.get("momentum_state") in ["bullish", "bearish"]:
            return {
                "detected": True,
                "confidence": 0.78,
                "side": "long" if mom["momentum_state"] == "bullish" else "short",
                "reason": "Momentum ignition detected"
            }

        return {"detected": False}

