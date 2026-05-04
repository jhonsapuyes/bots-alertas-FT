

# feature_engine/builders/feature_vector.py


def build_feature_vector(trend, momentum, volatility, price=None):
    """
    UNE FEATURES PURAS DEL MARKET
    NO toma decisiones
    NO clasifica mercado
    """

    # =========================
    # VALIDACIÓN SEGURA
    # =========================
    trend = trend or {}
    momentum = momentum or {}
    volatility = volatility or {}
    price = price or {}

    # =========================
    # NORMALIZACIÓN (solo estructura)
    # =========================

    return {
        "trend": {
            "trend_direction": trend.get("trend_direction"),
            "trend_strength": trend.get("trend_strength"),
            "structure_state": trend.get("structure_state"),
            "is_trending": trend.get("is_trending"),
            "bias": trend.get("bias"),
            "structure_score": trend.get("structure_score"),
            "trend_phase": trend.get("trend_phase"),
        },

        "momentum": {
            "momentum_state": momentum.get("momentum_state"),
            "momentum_strength": momentum.get("momentum_strength"),
            "entry_timing": momentum.get("entry_timing"),
            "continuation": momentum.get("continuation"),
            "rsi": momentum.get("rsi"),
        },

        "volatility": {
            "volatility_level": volatility.get("volatility_level"),
            "std_dev": volatility.get("std_dev"),
            "avg_range": volatility.get("avg_range"),
        },

        "price": {
            "last_open": price.get("last_open"),
            "last_close": price.get("last_close"),
            "last_high": price.get("last_high"),
            "last_low": price.get("last_low"),
            "range": price.get("range"),
            "body": price.get("body"),
            "direction": price.get("direction"),
        }
    }

