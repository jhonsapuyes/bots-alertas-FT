

# regime_engine/regime_classifier.py


def classify_regime(features: dict):
    """
    Regime Engine - robusto y alineado con feature_engine
    """

    # =========================
    # 🛡️ NORMALIZAR INPUT
    # =========================
    if not features:
        return {
            "trend_phase": "unknown",
            "market_regime": "range",
            "pressure": "neutral",
            "quality": "low"
        }

    # 🔥 FIX: soporta engine_output completo
    if "features" in features:
        features = features["features"]

    trend = features.get("trend", {})
    momentum = features.get("momentum", {})
    volatility = features.get("volatility", {})
    price = features.get("price", {})

    # =========================
    # EXTRAER FEATURES
    # =========================
    trend_direction = trend.get("trend_direction", "sideways")
    trend_phase = trend.get("trend_phase", "range")  # 🔥 fuente principal
    trend_strength = trend.get("trend_strength", "weak")
    structure_score = trend.get("structure_score", 0)
    is_trending = trend.get("is_trending", False)

    continuation = momentum.get("continuation", False)

    std = volatility.get("std_dev", 0)

    body = abs(price.get("body", 0))
    range_size = price.get("range", 0)

    # =========================
    # 🧠 1. CORRECCIÓN DE PHASE
    # =========================
    # 🔥 Evita incoherencias tipo: pullback + no trend
    if trend_phase == "pullback" and not is_trending:
        trend_phase = "transition"

    if trend_phase == "weak_trend" and trend_strength != "weak":
        trend_phase = "trend_continuation"

    # fallback inteligente
    if trend_phase not in ["trend_continuation", "pullback", "weak_trend", "range", "transition"]:
        if trend_direction in ["bullish", "bearish"]:
            trend_phase = "weak_trend"
        else:
            trend_phase = "range"

    # =========================
    # 🧭 2. MARKET REGIME
    # =========================
    if trend_phase in ["trend_continuation"]:
        market_regime = "trend"

    elif trend_phase == "pullback":
        # 🔥 sigue siendo tendencia pero no operable directo
        market_regime = "trend"

    elif trend_phase == "weak_trend":
        market_regime = "weak_trend"

    elif trend_phase == "transition":
        market_regime = "transition"

    else:
        market_regime = "range"

    # =========================
    # ⚖️ 3. PRESSURE
    # =========================
    if trend_direction == "bullish":
        pressure = "bullish"
    elif trend_direction == "bearish":
        pressure = "bearish"
    else:
        pressure = "neutral"

    # 🔥 si no hay estructura real → neutralizar
    if structure_score < 2:
        pressure = "neutral"

    # =========================
    # 📊 4. QUALITY SCORE
    # =========================
    quality_score = 0

    # 🔹 estructura (factor principal)
    quality_score += structure_score * 0.3

    # 🔹 continuidad real
    if continuation:
        quality_score += 1

    # 🔹 volatilidad útil (NO extrema)
    if 0.0015 < std < 0.009:
        quality_score += 1
    elif std >= 0.009:
        quality_score -= 0.5

    # 🔹 calidad de vela
    if range_size > 0:
        ratio = body / range_size

        if ratio > 0.55:
            quality_score += 1
        elif ratio < 0.2:
            quality_score -= 0.5

    # 🔹 penalización por pullback
    if trend_phase == "pullback":
        quality_score -= 0.5

    # =========================
    # 🏁 5. CLASIFICACIÓN FINAL
    # =========================
    if quality_score >= 2.5:
        quality = "high"
    elif quality_score >= 1.5:
        quality = "medium"
    else:
        quality = "low"

    # =========================
    # 📦 OUTPUT FINAL
    # =========================
    return {
        "trend_phase": trend_phase,
        "market_regime": market_regime,
        "pressure": pressure,
        "quality": quality
    }

