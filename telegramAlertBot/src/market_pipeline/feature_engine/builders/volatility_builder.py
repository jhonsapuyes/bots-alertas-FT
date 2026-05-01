

# feature_engine/builders/volatility_builder.py

def build_volatility_features(volatility_data):
    """
    Construye features de volatilidad a partir del output de volatility.py

    Args:
        volatility_data (dict): {
            "std_dev": float,
            "avg_range": float
        }

    Returns:
        dict
    """

    std_dev = volatility_data.get("std_dev", 0)
    avg_range = volatility_data.get("avg_range", 0)

    # Clasificación simple de volatilidad
    if std_dev < 0.002:
        volatility_level = "low"
    elif std_dev < 0.005:
        volatility_level = "medium"
    else:
        volatility_level = "high"

    return {
        "volatility_level": volatility_level,
        "std_dev": std_dev,
        "avg_range": avg_range
    }

