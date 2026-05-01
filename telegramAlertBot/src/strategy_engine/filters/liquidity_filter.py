

# strategy_engine/filters/liquidity_filter.py

from .base_filter import BaseFilter


class LiquidityFilter(BaseFilter):

    def apply(self, features: dict) -> dict:

        volatility = features["volatility"]

        # mercado muy lento
        if volatility["avg_range"] < 1:
            return {
                "passed": False,
                "reason": "low_liquidity_market",
                "meta": {}
            }

        return {
            "passed": True,
            "reason": None,
            "meta": {"liquidity": "ok"}
        }

