

from .data_adapter import normalize_candles
from .returns import calculate_returns
from .volatility import calculate_volatility
from .trend import calculate_trend
from .momentum import calculate_momentum

from .builders.trend_builder import build_trend_features
from .builders.momentum_builder import build_momentum_features
from .builders.volatility_builder import build_volatility_features

from strategy_engine.score_engine import calculate_score
from strategy_engine.market_scenarios import classify_market
from strategy_engine.decision_engine import generate_decision

# 🛑 FILTER LAYER
from strategy_engine.filters.filter_pipeline import FilterPipeline


def engine(raw_candles):

    # 📊 1. NORMALIZACIÓN
    candles = normalize_candles(raw_candles)

    # 📈 2. INDICADORES BASE
    returns = calculate_returns(candles)
    volatility = calculate_volatility(candles, returns)
    trend = calculate_trend(candles)
    momentum = calculate_momentum(candles)

    # 🧱 3. FEATURE BUILDERS
    trend_features = build_trend_features(trend)
    momentum_features = build_momentum_features(momentum)
    volatility_features = build_volatility_features(volatility)

    # 🧠 4. FEATURE UNIFICADO (INPUT DEL SISTEMA)
    features = {
        "trend": trend_features,
        "momentum": momentum_features,
        "volatility": volatility_features
    }

    # 🛑 5. FILTER PIPELINE (NUEVA CAPA CRÍTICA)
    filter_pipeline = FilterPipeline()
    filters_result = filter_pipeline.run(features)

    # ❌ SI NO PASA FILTROS → NO HAY TRADING
    if not filters_result["valid"]:
        return {
            "candles": candles,
            "features": features,
            "filters": filters_result,

            "score": None,
            "scenario": "filtered_out",
            "decision": {
                "action": "WAIT",
                "confidence": 0.5
            }
        }

    # 🎯 6. STRATEGY ENGINE (SOLO SI PASA FILTROS)
    score = calculate_score(features)
    scenario = classify_market(score, features)
    decision = generate_decision(score, scenario)

    # 📦 7. OUTPUT FINAL
    return {
        "candles": candles,

        "returns": returns,
        "volatility": volatility,
        "trend": trend,
        "momentum": momentum,

        "features": features,

        "filters": filters_result,

        "score": score,
        "scenario": scenario,
        "decision": decision
    }

