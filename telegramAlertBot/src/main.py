

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

from execution.execution import execute_trade_plan
from protetion_execution.protetion_execution import protect_execution
from storage.dataSave import save_pipeline_snapshot
from market_pipeline.data_fetch.get_market_data import get_market_data

from market_pipeline.data_fetch.data_adapter import normalize_candles
from market_pipeline.feature_engine.engine import engine
from market_pipeline.regime_engine.regime_classifier import classify_regime
from opportunity_engine.opportunity_engine import run_opportunity_engine
from risk_engine.risk_engine import build_risk
from signal_translation.signal_translator import translate_signal

from confirmation_filter.confirmation_filter import evaluate_confirmation
from strategy_engine.strategy_engine import build_strategy
from trade_planner.trade_planner import build_trade_plan


def main():
    input_dataSave = {}

    symbol = "ETHUSDT"
    interval = "1h"

    raw_data = get_market_data(
        symbol=symbol,
        interval=interval,
        limit=10,
        retries=3
    )
    input_dataSave["raw_data"] = raw_data

    candles = normalize_candles(raw_data)
    input_dataSave["candles"] = candles

    engine_output = engine(candles)
    input_dataSave["engine"] = engine_output

    regime_output = classify_regime(engine_output)
    input_dataSave["regime"] = regime_output

    opportunities = run_opportunity_engine(
        features=engine_output,
        regime=regime_output
    )
    input_dataSave["opportunities"] = opportunities

    # 🔥 SIGNAL TRANSLATION LAYER
    signals = []
    for opp in opportunities:
        signal = translate_signal(
            opportunity=opp,
            features=engine_output["features"],
            regime=regime_output
        )
        signals.append(signal)
    input_dataSave["signals"] = signals

    confirmation = evaluate_confirmation({
        "features": engine_output["features"],
        "regime": regime_output,
        "signal": signals[0],
        "opportunity": opportunities[0]
    })
    input_dataSave["confirmation"] = confirmation


    strategy = build_strategy({
        "signal": signal,
        "confirmation": confirmation,
        "features": engine_output["features"],
        "regime": regime_output
    })
    input_dataSave["strategy"] = strategy


    #save_pipeline_snapshot(symbol,input_dataSave)
    

    risk= build_risk({
        "strategy": strategy,              
        "confirmation": confirmation,
        "features": engine_output["features"],
        "regime": regime_output
    })


    trade_plan = build_trade_plan({
        "features": engine_output["features"],
        "regime": regime_output,
        "signal": signal,
        "confirmation": confirmation,
        "strategy": strategy,
        "risk": risk
    })


    execution_result = execute_trade_plan(
    trade_plan=trade_plan,
    exchange="binance",
    symbol="ETHUSDT"
    )

    protection = protect_execution(
        execution_result
    )


    def screenPrint(pt1): 
        if(pt1=="all"):
            print("main-input_dataSave", input_dataSave)
        elif(pt1=="one"):
            print("main-raw_data", raw_data)
            print("main-candles", candles)
            print("main-engine", engine_output)
            print("main-regime", regime_output)
            print("main-opportunities", opportunities)
            print("main-signals", signals)
            print("main-confirmation", confirmation)
            print("main-strategy", strategy)
            print("main-risk", risk)
            print("main-trade-plan", trade_plan)
            print("main-execution", execution_result)
            print("main-protection",protection)

    screenPrint("one")

if __name__ == "__main__":
    main()
