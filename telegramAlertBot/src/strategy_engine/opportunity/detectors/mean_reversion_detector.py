

from ..base_detector import BaseDetector


class MeanReversionDetector(BaseDetector):
    name = "mean_reversion"

    def detect(self, features, market):
        mom = features.get("momentum", {})

        if mom.get("rsi", 50) > 70:
            return {
                "detected": True,
                "confidence": 0.75,
                "side": "short",
                "reason": "Overbought mean reversion"
            }

        if mom.get("rsi", 50) < 30:
            return {
                "detected": True,
                "confidence": 0.75,
                "side": "long",
                "reason": "Oversold mean reversion"
            }

        return {"detected": False}

