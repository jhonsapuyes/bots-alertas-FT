

# core/pipeline.py

from strategy_engine.filters.filter_pipeline import FilterPipeline
from strategy_engine.opportunity.opportunity_engine import OpportunityEngine


filter_pipeline = FilterPipeline()
opportunity_engine = OpportunityEngine()


def run_pipeline(engine_output: dict) -> dict:
    """
    PIPELINE: SOLO PROCESA DATA YA GENERADA POR ENGINE
    """

    features = engine_output["features"]

    # 1. FILTERS (GATEKEEPER)
    filter_result = filter_pipeline.run(features)

    if not filter_result.get("valid", False):
        return {
            "status": "rejected_by_filters",
            "filters": filter_result,
            "features": features
        }

    # 2. OPPORTUNITIES
    opportunities = opportunity_engine.run(
        features=features,
        market=engine_output
    )

    # 3. OUTPUT FINAL
    return {
        "status": "ok",
        "features": features,
        "filters": filter_result,
        "opportunities": opportunities
    }

