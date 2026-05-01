

def decision_engine(ctx):

    data = ctx.get("data", {})
    analysis = ctx.get("analysis", {})
    scenarios = ctx.get("scenarios", {})  # 👈 ahora usamos escenarios completos
    bias = data.get("bias", {})
    fatigue = ctx.get("fatigue", None)

    # =========================
    # 🧠 1. FATIGUE FILTER (PRIORIDAD MÁXIMA)
    # =========================
    if fatigue:
        if fatigue.get("phase") == "exhaustion":

            reversal = scenarios.get("reversal", {})

            if not reversal.get("active"):
                return {
                    "buy": False,
                    "sell": False,
                    "reason": "fatigue_block",
                    "stage": "blocked_by_fatigue"
                }

    # =========================
    # 🧠 2. FILTRO POR MARKET BIAS
    # =========================
    market_type = bias.get("scenario", "unknown")

    allowed = []

    for name, sc in scenarios.items():

        if not sc.get("active"):
            continue

        # 🔥 MAPEAMOS ESCENARIO vs BIAS
        if market_type == "range" and name == "range":
            allowed.append(sc)

        elif market_type == "trend_continuation" and name in ["trend", "pullback"]:
            allowed.append(sc)

        elif market_type == "possible_reversal" and name == "reversal":
            allowed.append(sc)

        elif market_type == "breakout" and name == "breakout":
            allowed.append(sc)

        elif market_type == "unknown":
            allowed.append(sc)

    # si no hay nada válido
    if not allowed:
        return {
            "buy": False,
            "sell": False,
            "reason": "no_valid_opportunities",
            "stage": "bias_filtered_empty"
        }

    # =========================
    # 🧠 3. SELECCIÓN DEL MEJOR ESCENARIO
    # =========================
    best = max(allowed, key=lambda x: x.get("score", 0))

    # =========================
    # 🧠 4. VALIDACIÓN FINAL (ANTI-CONFLICTOS)
    # =========================
    macd_bear = analysis.get("macd_bear", False)
    macd_bull = analysis.get("macd_bull", False)

    if best.get("buy") and macd_bear:
        return {
            "buy": False,
            "sell": False,
            "reason": "conflict_macd_bear",
            "stage": "rejected"
        }

    if best.get("sell") and macd_bull:
        return {
            "buy": False,
            "sell": False,
            "reason": "conflict_macd_bull",
            "stage": "rejected"
        }

    # =========================
    # 🧠 5. RESULTADO FINAL
    # =========================
    return {
        "buy": best.get("buy", False),
        "sell": best.get("sell", False),
        "reason": best.get("reason", "decision_engine"),
        "entry_type": best.get("entry_type"),
        "score": best.get("score", 0),
        "scenario": best.get("type"),
        "stage": "approved"
    }

