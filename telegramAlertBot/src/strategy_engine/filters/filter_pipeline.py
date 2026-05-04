

# strategy_engine/filters/filter_pipeline.py

from .noise_filter import NoiseFilter
from .regime_filter import RegimeFilter
from .liquidity_filter import LiquidityFilter
from .volatility_filter import VolatilityFilter
from .structure_filter import StructureFilter


class FilterPipeline1:

    def __init__(self):
        self.filters = [
            NoiseFilter(),
            RegimeFilter(),
            LiquidityFilter(),
            VolatilityFilter(),
            StructureFilter()
        ]

    def run(self, features: dict) -> dict:
        print("FilterPipeline",features)

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

    # ----------------------------
    # 🔧 NORMALIZACIÓN DE SCHEMA
    # ----------------------------
    def _normalize(self, features: dict) -> dict:
        """
        Unifica estructura para evitar errores de keys inconsistentes
        """

        return {
            "trend": features.get("features", {}).get("trend") 
                     or features.get("trend"),

            "momentum": features.get("features", {}).get("momentum") 
                        or features.get("momentum"),

            "volatility": features.get("features", {}).get("volatility") 
                          or features.get("volatility"),

            "price": features.get("features", {}).get("price") 
                     or features.get("price"),

            "market_state": features.get("features", {}).get("market_state") 
                            or features.get("market_state"),
        }

    # ----------------------------
    # 🚀 PIPELINE PRINCIPAL
    # ----------------------------
    def run(self, features: dict) -> dict:

        #print("FilterPipeline INPUT:", features)

        features = self._normalize(features)

        reasons = []
        meta = {
            "errors": [],
            "passed_filters": [],
            "failed_filters": []
        }

        score_penalty = 0.0

        for f in self.filters:

            filter_name = f.__class__.__name__

            try:
                result = f.apply(features)

                passed = result.get("passed", True)

                # ----------------------------
                # ❌ FAIL
                # ----------------------------
                if not passed:
                    reason = result.get("reason", "unknown")
                    reasons.append(reason)
                    meta["failed_filters"].append(filter_name)

                    score_penalty += 0.15

                # ----------------------------
                # ✅ PASS
                # ----------------------------
                else:
                    meta["passed_filters"].append(filter_name)

                # merge metadata sin sobrescribir
                if result.get("meta"):
                    meta.update({
                        f"{filter_name}_meta": result["meta"]
                    })

            except Exception as e:

                # 🔥 error aislado por filtro
                meta["errors"].append({
                    "filter": filter_name,
                    "error": str(e)
                })

                reasons.append(f"{filter_name}_error")
                score_penalty += 0.25

        # ----------------------------
        # 🎯 SCORE FINAL (NO BINARIO)
        # ----------------------------
        base_score = 1.0
        final_score = max(0.0, base_score - score_penalty)

        # ----------------------------
        # 🧠 DECISIÓN FINAL
        # ----------------------------
        valid = final_score >= 0.5 and len(meta["errors"]) == 0

        return {
            "valid": valid,
            "score": round(final_score, 3),
            "reasons": reasons,
            "meta": meta
        }