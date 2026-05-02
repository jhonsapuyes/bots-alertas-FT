

    #coins = [
    #"BTCUSDT",
    #"ETHUSDT",
    #"BNBUSDT",
    #"SOLUSDT",
    #"XRPUSDT",
    #"ADAUSDT",
    #"DOGEUSDT",
    #"MATICUSDT",
    #"LTCUSDT",
    #"AVAXUSDT"
    #]

from market_pipeline.data_fetch.get_market_data import get_market_data

from core.pipeline import run_pipeline
from market_pipeline.feature_engine.data_adapter import normalize_candles
from market_pipeline.feature_engine.engine import engine

from trade_planner.trade_planner import TradePlanner


def main():

    from datetime import datetime

    # -----------------------------
    # 1. DATA INPUT
    # -----------------------------
    symbol = "ETHUSDT"
    interval = "1h"

    raw_data = get_market_data(
        symbol=symbol,
        interval=interval,
        limit=10,
        retries=3
    )

    candles = normalize_candles(raw_data)
    current_price = candles[-1]["close"]

    # -----------------------------
    # 2. PIPELINE
    # -----------------------------
    engine_output = engine(candles)
    result = run_pipeline(engine_output)

    trade_planner = TradePlanner()

    trade_plan = trade_planner.plan(
        features=result.get("features", {}),
        decision=result.get("decision", {}),
        price=current_price
    )

    # -----------------------------
    # 3. TIME CONTEXT
    # -----------------------------
    now = datetime.now()

    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    # -----------------------------
    # 4. DATA CLAVE
    # -----------------------------
    decision = result.get("decision", {})

    side = trade_plan.get("side")
    confidence = decision.get("confidence")
    bias = decision.get("bias")
    regime = decision.get("regime")
    signal = decision.get("active_signal")

    entry = trade_plan.get("entry_zone")
    sl = trade_plan.get("stop_loss")
    tp = trade_plan.get("take_profit")

    # -----------------------------
    # 5. VISIÓN DE TRADING
    # -----------------------------
    print("\n" + "🔥" * 40)
    print(f"📅 DATE: {date_str} | ⏰ TIME: {time_str}")
    print(f"📊 MARKET: {symbol} | TF: {interval}")
    print(f"💰 PRICE: {current_price}")
    print("-" * 40)

    if side == "LONG":
        print("🟢 SIGNAL: LONG SETUP DETECTED")
    elif side == "SHORT":
        print("🔴 SIGNAL: SHORT SETUP DETECTED")
    else:
        print("🟡 SIGNAL: NO CLEAR TRADE")

    print(f"📡 REGIME: {regime}")
    print(f"📈 BIAS: {bias}")
    print(f"⚡ ACTIVE SIGNAL: {signal}")
    print(f"🎯 CONFIDENCE: {confidence}")

    print("-" * 40)

    print("📍 ENTRY ZONE:", entry)
    print("🛑 STOP LOSS:", sl)

    if tp:
        print("🎯 TAKE PROFIT 1:", tp.get("tp1"))
        print("🎯 TAKE PROFIT 2:", tp.get("tp2"))

    print("-" * 40)

    print(f"📊 POSITION SIZE: {trade_plan.get('position_size')}")
    print(f"⚙️ MODE: {trade_plan.get('execution_mode')}")

    print("🔥" * 40)

    return {
        "date": date_str,
        "time": time_str,
        "symbol": symbol,
        "price": current_price,
        "trade_plan": trade_plan,
        "decision": decision
    }


if __name__ == "__main__":
    main()
