

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

from core.analysisRun import analysisRun
from execution.decision_engine import decision_engine
from execution.decide_trade import decide_trade
from execution.build_trade import build_trade

#from execution.trend_fatigue_detector import TrendFatigueDetector

from datetime import datetime
import time


def main1():

    coins = ["ETHUSDT"]

    # detector = TrendFatigueDetector()

    loop=0
    while True:

        for coin in coins:

            print(f"\n🪙 {coin} | {datetime.now()}")

            # =========================
            # 🧠 1. ANALYSIS
            # =========================
            data = analysisRun(coin)
            print("analysisRun:", data)
            #print("analysisRun:", data["layers"])

            ##if "error" in data:
            ##    print("ERROR:", data)
            ##    continue
##
            ### =========================
            ### 🧠 2. FATIGUE
            ### =========================
            ##fatigue = detector.analyze(coin, data)
##
            ### =========================
            ### 🧠 3. CONTEXTO GLOBAL
            ### =========================
            ##ctx = {
            ##    "data": data,
            ##    "analysis": data.get("analysis"),
            ##    "opportunities": data.get("opportunities"),
            ##    "fatigue": fatigue
            ##}
##
            ##print("SCENARIOS:", data.get("scenarios"))
            ##print("FATIGUE:", fatigue)
##
            ### =========================
            ### 🧠 4. DECISION ENGINE
            ### =========================
            ##decision = decision_engine(ctx)
            ##print("DECISION:", decision)
##
            ### =========================
            ### 🧠 5. FILTRO (decide_trade)
            ### =========================
            ##filtered = decide_trade(ctx, decision)
##
            ##if not filtered:
            ##    print("🚫 NO TRADE (filtered)")
            ##    continue
##
            ### =========================
            ### 🔥 6. TRADE PLANNER
            ### =========================
            ##trade = build_trade(ctx, filtered, capital=100)
##
            ##if not trade:
            ##    print("🚫 NO TRADE (planner reject)")
            ##    continue
##
            ### =========================
            ### ✅ RESULTADO FINAL
            ### =========================
            ##print("🚀 TRADE:", trade)

        time.sleep(3)

        loop += 1
        if loop == 1:
            break


from market_pipeline.data_fetch.get_market_data import get_market_data
from market_pipeline.feature_engine.engine import engine

def main():

    raw_data = get_market_data("ETHUSDT")
    print("get_market_data:", raw_data)

    features = engine(raw_data)
    print("engine:", features)


if __name__ == "__main__":
    main()

