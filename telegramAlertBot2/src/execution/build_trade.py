

def build_trade(ctx, decision, capital=100, risk_per_trade=0.01):
    """
    Construye un trade REAL a partir de:
    - contexto (ctx)
    - decisión del decision_engine

    Devuelve:
    - señal completa con entry, SL, TP, size, RR
    """

    if not decision or (not decision.get("buy") and not decision.get("sell")):
        return None

    data = ctx.get("data", {})
    price = data.get("price")
    volatility = data.get("volatility", 0)
    trend = data.get("trend")

    if not price:
        return None

    action = "BUY" if decision.get("buy") else "SELL"

    # =========================
    # 🎯 1. ENTRY
    # =========================
    entry = price
    entry_type = decision.get("entry_type", "market")

    # =========================
    # 🛑 2. STOP LOSS
    # =========================
    # basado en volatilidad (más robusto que fijo)
    if volatility == 0:
        volatility = 0.01  # fallback

    sl_distance = volatility * 1.5

    if action == "BUY":
        stop_loss = entry * (1 - sl_distance)
    else:
        stop_loss = entry * (1 + sl_distance)

    # =========================
    # 🎯 3. TAKE PROFIT
    # =========================
    rr_target = 2  # riesgo beneficio mínimo

    if action == "BUY":
        risk = entry - stop_loss
        take_profit = entry + (risk * rr_target)
    else:
        risk = stop_loss - entry
        take_profit = entry - (risk * rr_target)

    # =========================
    # ⚖️ 4. VALIDACIÓN RR
    # =========================
    if risk <= 0:
        return None

    reward = abs(take_profit - entry)
    rr = reward / risk

    if rr < 1.5:
        return None  # trade malo

    # =========================
    # 💰 5. POSITION SIZE
    # =========================
    risk_amount = capital * risk_per_trade

    position_size = risk_amount / risk

    # =========================
    # 🚫 6. FILTROS EXTRA
    # =========================
    # evitar mercado muerto
    if volatility < 0.002:
        return None

    # evitar movimientos extremos
    if volatility > 0.2:
        return None

    # =========================
    # 📦 7. RESULTADO FINAL
    # =========================
    return {
        "action": action,
        "entry": round(entry, 4),
        "entry_type": entry_type,
        "stop_loss": round(stop_loss, 4),
        "take_profit": round(take_profit, 4),
        "rr": round(rr, 2),
        "risk_per_trade": risk_per_trade,
        "position_size": round(position_size, 6),
        "confidence": decision.get("strength", "unknown"),
        "reason": decision.get("reason"),
        "scenario": decision.get("scenario"),
    }

