

def build_trend_features1(trend_data):

    if not trend_data:
        return {}

    direction = trend_data.get("direction", "sideways")
    strength = trend_data.get("strength", "neutral")
    structure_state = trend_data.get("structure_state", "sideways")

    higher_highs = trend_data.get("higher_highs", 0)
    higher_lows = trend_data.get("higher_lows", 0)
    lower_highs = trend_data.get("lower_highs", 0)
    lower_lows = trend_data.get("lower_lows", 0)

    # DERIVED LAYER (OK aquí)
    bias = (
        "long" if direction == "bullish"
        else "short" if direction == "bearish"
        else "neutral"
    )

    is_trending = (
        direction in ["bullish", "bearish"]
        and strength == "strong"
    )

    structure_score = (higher_highs + higher_lows) - (lower_highs + lower_lows)

    return {
        "trend_direction": direction,
        "trend_strength": strength,
        "structure_state": structure_state,
        "is_trending": is_trending,
        "bias": bias,
        "structure_score": structure_score
    }


def build_trend_features2(trend_data):

    if not trend_data:
        return {}

    direction = trend_data.get("direction", "sideways")
    strength = trend_data.get("strength", "neutral")
    structure_state = trend_data.get("structure_state", "sideways")

    higher_highs = trend_data.get("higher_highs", 0)
    higher_lows = trend_data.get("higher_lows", 0)
    lower_highs = trend_data.get("lower_highs", 0)
    lower_lows = trend_data.get("lower_lows", 0)

    # =========================
    # BIAS (DERIVADO OK)
    # =========================
    bias = (
        "long" if direction == "bullish"
        else "short" if direction == "bearish"
        else "neutral"
    )

    # =========================
    # STRUCTURE DELTA (BASE REAL)
    # =========================
    structure_delta = (higher_highs + higher_lows) - (lower_highs + lower_lows)

    total_moves = higher_highs + higher_lows + lower_highs + lower_lows

    # =========================
    # IS_TRENDING (FIX REAL)
    # =========================
    is_trending = (
        direction in ["bullish", "bearish"]
        and total_moves > 0
        and abs(structure_delta) / total_moves > 0.15
    )

    # =========================
    # STRUCTURE SCORE
    # =========================
    structure_score = structure_delta

    return {
        "trend_direction": direction,
        "trend_strength": strength,
        "structure_state": structure_state,
        "is_trending": is_trending,
        "bias": bias,
        "structure_score": structure_score
    }


# =========================================================
# 2. FEATURE LAYER (NO RAW LOGIC HERE)
# =========================================================
def build_trend_features(trend_data):

    if not trend_data:
        return {}

    direction = trend_data["direction"]
    strength = trend_data["strength"]
    structure_state = trend_data["structure_state"]

    hh = trend_data["higher_highs"]
    hl = trend_data["higher_lows"]
    lh = trend_data["lower_highs"]
    ll = trend_data["lower_lows"]

    # -------------------------
    # BIAS (DERIVED ONLY HERE)
    # -------------------------
    bias = (
        "long" if direction == "bullish"
        else "short" if direction == "bearish"
        else "neutral"
    )

    # -------------------------
    # STRUCTURE INTENSITY
    # -------------------------
    delta = (hh + hl) - (lh + ll)
    total = hh + hl + lh + ll

    # -------------------------
    # IS TRENDING (FIX REAL)
    # -------------------------
    # NO depende solo de strength
    is_trending = (
        direction in ["bullish", "bearish"]
        and total > 0
        and abs(delta) / total > 0.20
    )

    # -------------------------
    # TREND PHASE (NUEVO)
    # -------------------------
    # AQUÍ ENTRA LO QUE PEDÍAS: pullback / continuation
    if structure_state.endswith("recovery"):
        phase = "pullback"
    elif is_trending and strength == "strong":
        phase = "continuation"
    elif is_trending and strength == "weak":
        phase = "weak_trend"
    else:
        phase = "range"

    return {
        "trend_direction": direction,
        "trend_strength": strength,
        "structure_state": structure_state,
        "is_trending": is_trending,
        "bias": bias,
        "structure_score": delta,
        "trend_phase": phase
    }

