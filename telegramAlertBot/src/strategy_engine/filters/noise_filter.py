

# strategy_engine/filters/noise_filter.py

from .base_filter import BaseFilter


class NoiseFilter(BaseFilter):

    def apply(self, features: dict) -> dict:

        trend = features["trend"]
        momentum = features["momentum"]

        # señal débil / sin estructura
        if trend["structure_score"] <= 2 and abs(momentum["rsi"] - 50) < 5:
            return {
                "passed": False,
                "reason": "low_signal_quality",
                "meta": {}
            }

        return {
            "passed": True,
            "reason": None,
            "meta": {"noise": "clean"}
        }

