

from .returns import calculate_returns
from .volatility import calculate_volatility
from .trend import calculate_trend
from .momentum import calculate_momentum

from .indicadores.indicator_engine import calculate_indicators

from .builders.trend_builder import build_trend_features,build_trend_features1
from .builders.momentum_builder import build_momentum_features
from .builders.volatility_builder import build_volatility_features
from .builders.price_builder import build_price_features
from .builders.feature_vector import build_feature_vector

from strategy_engine.score_engine import calculate_score
from strategy_engine.market_scenarios import classify_market
from strategy_engine.decision_engine import generate_decision

from strategy_engine.filters.filter_pipeline import FilterPipeline

from market_pipeline.regime_engine.regime_classifier import classify_regime


def engine1(raw_candles):

    # =========================
    # 1. DATA
    # =========================
    candles = raw_candles

    # =========================
    # 2. BASE CALCULATIONS
    # =========================
    returns = calculate_returns(candles)

    indicators = calculate_indicators(candles)

    volatility = calculate_volatility(candles, returns, indicators)
    trend = calculate_trend(candles, indicators)
    momentum = calculate_momentum(candles, indicators)

    # =========================
    # 3. BUILDERS
    # =========================
    trend_features = build_trend_features(trend)
    momentum_features = build_momentum_features(momentum)
    volatility_features = build_volatility_features(volatility)
    price_features = build_price_features(candles)

    # =========================
    # 4. FEATURE VECTOR
    # =========================
    features = build_feature_vector(
        trend=trend_features,
        momentum=momentum_features,
        volatility=volatility_features,
        price=price_features
    )

    # =========================
    # 5. FILTER PIPELINE
    # =========================

    pipeline_input = {
        "features": features,

        "market_data": {
            "returns": returns,
            "candles": candles
        }
    }



    filter_pipeline = FilterPipeline()
    # 🔥 IMPORTANTE: ahora también le pasamos contexto real
    filters_result = filter_pipeline.run(pipeline_input)

    # 🆕 REGIME LAYER (CLAVE)
    regime = classify_regime(filters_result, features)
    #print("engine",regime)


    # ❌ BLOQUEO
    if not filters_result["valid"]:
        return {
            "candles": candles,
            "returns": returns,
            "volatility": volatility,
            "trend": trend,
            "momentum": momentum,
            "features": features,
            "filters": filters_result,
            "regime": regime,
            "score": None,
            "scenario": "filtered_out",
            "decision": {
                "action": "WAIT",
                "confidence": 0.5
            }
        }

    # =========================
    # 6. STRATEGY ENGINE
    # =========================
    score = calculate_score(features, regime)  # 👈 MEJORA IMPORTANTE
    scenario = classify_market(score, features, regime)
    decision = generate_decision(score, scenario)

    # =========================
    # 7. OUTPUT FINAL
    # =========================
    return {
        "candles": candles,
        "returns": returns,
        "volatility": volatility,
        "trend": trend,
        "momentum": momentum,
        "features": features,
        "filters": filters_result,
        "regime": regime,   # 👈 NUEVO
        "score": score,
        "scenario": scenario,
        "decision": decision
    }


def engine(raw_candles):

    # =========================
    # 1. VALIDACIÓN
    # =========================
    candles = raw_candles

    if not candles or len(candles) < 5:
        return {
            "features": None,
            "debug": None,
            "error": "insufficient_data"
        }

    # =========================
    # 2. BASE CALCULATIONS (PURE DATA LAYER)
    # =========================
    returns = calculate_returns(candles)
    indicators = calculate_indicators(candles)

    volatility_raw = calculate_volatility(candles, returns, indicators)
    trend_raw = calculate_trend(candles, indicators)
    momentum_raw = calculate_momentum(candles, indicators)
    #print("engine-calculate",volatility_raw,trend_raw,momentum_raw)

    # =========================
    # 3. BUILDERS (INTERPRETATION MATHEMATICAL ONLY)
    # =========================
    trend_features = build_trend_features(trend_raw)
    momentum_features = build_momentum_features(momentum_raw)
    volatility_features = build_volatility_features(volatility_raw)
    price_features = build_price_features(candles)
    #print("engine-builders",trend_features,momentum_features,volatility_features,price_features)

    # =========================
    # 4. FEATURE VECTOR (FINAL CONTRACT)
    # =========================
    features = build_feature_vector(
        trend=trend_features,
        momentum=momentum_features,
        volatility=volatility_features,
        price=price_features
    )
    #print("engine-features",features)


    # =========================
    # 5. DEBUG LAYER (OPTIONAL OBSERVABILITY ONLY)
    # =========================
    debug = {
        "returns": returns,
        "trend_raw": trend_raw,
        "momentum_raw": momentum_raw,
        "volatility_raw": volatility_raw
    }

    # =========================
    # 6. OUTPUT (PURE FEATURE ENGINE OUTPUT)
    # =========================
    return {
        "features": features,
        "debug": debug
    }

