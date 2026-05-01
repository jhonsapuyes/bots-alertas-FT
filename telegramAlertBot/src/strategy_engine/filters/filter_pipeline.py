

# strategy_engine/filters/filter_pipeline.py

from .noise_filter import NoiseFilter
from .regime_filter import RegimeFilter
from .liquidity_filter import LiquidityFilter
from .volatility_filter import VolatilityFilter
from .structure_filter import StructureFilter


class FilterPipeline:

    def __init__(self):
        self.filters = [
            NoiseFilter(),
            RegimeFilter(),
            LiquidityFilter(),
            VolatilityFilter(),
            StructureFilter()
        ]

    def run(self, features: dict) -> dict:

        reasons = []
        meta = {}

        for f in self.filters:
            try:
                result = f.apply(features)

                if not result.get("passed", True):
                    reasons.append(result.get("reason"))

                meta.update(result.get("meta", {}))

            except Exception as e:
                # 🔥 IMPORTANTE: nunca romper el engine por un filter
                reasons.append(f"{f.__class__.__name__}_error")
                meta["error"] = str(e)

        return {
            "valid": len(reasons) == 0,
            "reasons": reasons,
            "meta": meta
        }
    
    