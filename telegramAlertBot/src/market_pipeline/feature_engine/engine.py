

from .data_adapter import normalize_candles
from .returns import calculate_returns
from .volatility import calculate_volatility
from .trend import calculate_trend
from .momentum import calculate_momentum

from .builders.trend_builder import build_trend_features
from .builders.momentum_builder import build_momentum_features
from .builders.volatility_builder import build_volatility_features
from .builders.feature_vector import build_feature_vector


def engine(raw_candles):

    candles = normalize_candles(raw_candles)

    returns = calculate_returns(candles)
    volatility = calculate_volatility(candles, returns)
    trend = calculate_trend(candles)
    momentum = calculate_momentum(candles)

    # 🔥 builders
    trend_features = build_trend_features(trend)
    momentum_features = build_momentum_features(momentum)
    volatility_features = build_volatility_features(volatility)

    # 🧠 decisión final
    feature_vector = build_feature_vector(
        trend_features,
        momentum_features,
        volatility_features
    )

    return {
        "candles": candles,
        "returns": returns,
        "volatility": volatility,
        "trend": trend,
        "momentum": momentum,

        "features": {
            "trend": trend_features,
            "momentum": momentum_features,
            "volatility": volatility_features
        },

        # 🔥 OUTPUT FINAL
        "decision": feature_vector
    }

