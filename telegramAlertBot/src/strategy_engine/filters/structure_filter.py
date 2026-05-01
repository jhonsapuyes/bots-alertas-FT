

# strategy_engine/filters/structure_filter.py

from .base_filter import BaseFilter


class StructureFilter(BaseFilter):

    def apply(self, features: dict) -> dict:

        trend = features["trend"]

        # 🧠 SAFE ACCESS (evita KeyError)
        structure = trend.get("structure", {})

        higher_lows = structure.get("higher_lows", 0)
        lower_lows = structure.get("lower_lows", 0)
        higher_highs = structure.get("higher_highs", 0)

        # 🔥 lógica simplificada pero estable
        if lower_lows > higher_lows and not trend["is_trending"]:
            return {
                "passed": False,
                "reason": "structure_broken",
                "meta": {
                    "lower_lows": lower_lows,
                    "higher_lows": higher_lows
                }
            }

        return {
            "passed": True,
            "reason": None,
            "meta": {"structure": "ok"}
        }
    
    