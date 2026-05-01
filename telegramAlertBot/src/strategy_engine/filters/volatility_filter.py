

# strategy_engine/filters/volatility_filter.py

from .base_filter import BaseFilter


class VolatilityFilter(BaseFilter):

    def apply(self, features: dict) -> dict:

        volatility = features["volatility"]

        std = volatility["std_dev"]

        # demasiado riesgo (spikes / noticias)
        if std > 0.01:
            return {
                "passed": False,
                "reason": "high_volatility_risk",
                "meta": {"risk": "too_high"}
            }

        # demasiado plano
        if std < 0.0005:
            return {
                "passed": False,
                "reason": "dead_market",
                "meta": {"risk": "too_low"}
            }

        return {
            "passed": True,
            "reason": None,
            "meta": {"volatility": "acceptable"}
        }

