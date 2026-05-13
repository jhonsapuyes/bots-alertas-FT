

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

