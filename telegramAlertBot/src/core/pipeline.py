
# core/pipeline.py

from strategy_engine.filters.filter_pipeline import FilterPipeline
from strategy_engine.opportunity.opportunity_engine import OpportunityEngine
from core.decision_layer.signal_arbitrator import SignalArbitrator


filter_pipeline = FilterPipeline()
opportunity_engine = OpportunityEngine()
arbitrator = SignalArbitrator()


def run_pipeline(engine_output: dict) -> dict:
    """
    PIPELINE:
    engine → filters → opportunities → arbitrator (DECISION LAYER)
    """

    # -----------------------------
    # 0. INPUT
    # -----------------------------
    features = engine_output.get("features", {})

    # -----------------------------
    # 1. FILTERS (GATEKEEPER)
    # -----------------------------
    filter_result = filter_pipeline.run(features)

    if not filter_result.get("valid", False):
        return {
            "status": "rejected_by_filters",
            "filters": filter_result,
            "features": features
        }

    # -----------------------------
    # 2. OPPORTUNITIES (MULTI-HIPÓTESIS)
    # -----------------------------
    opportunities = opportunity_engine.run(
        features=features,
        market=engine_output
    )

    # -----------------------------
    # 3. DECISION LAYER (ARBITRATOR)
    # -----------------------------
    decision = arbitrator.run({
        "features": features,
        "filters": filter_result,
        "opportunities": opportunities
    })

    # -----------------------------
    # 4. OUTPUT FINAL UNIFICADO
    # -----------------------------
    return {
        "status": "ok",
        "features": features,
        "filters": filter_result,
        "opportunities": opportunities,
        "decision": decision
    }

