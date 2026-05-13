

from risk_engine.risk_engine import build_risk
from strategy_engine.strategy_engine import build_strategy
from trade_planner.trade_planner import build_trade_plan


def strategyLayer_execute(pt1,pt2): 
    resp_strategyLayer={}
    resp_strategyLayer["strategy"]= strategy(pt2["signal"][0],pt2["confirmation"],pt1["features"],pt2["regime"])
    resp_strategyLayer["risk"]= risk(resp_strategyLayer["strategy"],pt2["confirmation"],pt1["features"],pt2["regime"])
    resp_strategyLayer["trade_plan"]= trade_plan(pt1["features"],pt2["regime"],pt2["signal"][0],pt2["confirmation"],resp_strategyLayer["strategy"],resp_strategyLayer["risk"])
    return resp_strategyLayer


def strategy(signal,confirmation,engine,regime):
    return build_strategy({
        "signal": signal,
        "confirmation": confirmation,
        "features": engine,
        "regime": regime
    })


def risk(strategy,confirmation,engine,regime):
    return build_risk({
        "strategy": strategy,              
        "confirmation": confirmation,
        "features": engine,
        "regime": regime
    })


def trade_plan(engine,regime,signal,confirmation,strategy,risk):
    return build_trade_plan({
        "features": engine,
        "regime": regime,
        "signal": signal,
        "confirmation": confirmation,
        "strategy": strategy,
        "risk": risk
    })

