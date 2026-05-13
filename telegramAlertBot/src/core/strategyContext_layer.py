

from risk_engine.risk_engine import build_risk
from strategy_context.strategy_context import strategy_context
from trade_planner.trade_planner import build_trade_plan


def strategyContextLayer_execute(pt1,pt2,pt3):    
    resp_strategyContextLayer={}
    resp_strategyContextLayer["strategy_context"]= strategyContext(pt1["features"],pt2,pt3)
    resp_strategyContextLayer["risk_context"]= riskContext(resp_strategyContextLayer["strategy_context"],pt2["confirmation"],pt1["features"],pt2["regime"])
    resp_strategyContextLayer["tradePlan_context"]= tradePlan_context(pt1["features"],pt2["regime"],pt2["signal"][0],pt2["confirmation"],resp_strategyContextLayer["strategy_context"],resp_strategyContextLayer["risk_context"])

    return resp_strategyContextLayer


def strategyContext(features,market_analysis,adaptive_context):
    return strategy_context(
        features,
        market_analysis,
        adaptive_context
    )


def riskContext(strategy,confirmation,engine,regime):
    return build_risk({
        "strategy": strategy,              
        "confirmation": confirmation,
        "features": engine,
        "regime": regime
    })

def tradePlan_context(engine,regime,signal,confirmation,strategy,risk):
    return build_trade_plan({
        "features": engine,
        "regime": regime,
        "signal": signal,
        "confirmation": confirmation,
        "strategy": strategy,
        "risk": risk
    })

