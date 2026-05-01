

# strategy_engine/filters/regime_filter.py

from .base_filter import BaseFilter


class RegimeFilter(BaseFilter):

    def apply(self, features: dict) -> dict:

        trend = features["trend"]
        momentum = features["momentum"]

        # mercado sin dirección clara
        if not trend["is_trending"] and momentum["momentum_state"] == "neutral":
            return {
                "passed": False,
                "reason": "sideways_low_edge_market",
                "meta": {"regime": "sideways"}
            }

        return {
            "passed": True,
            "reason": None,
            "meta": {"regime": "tradable"}
        }

