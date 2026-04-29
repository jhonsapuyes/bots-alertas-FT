

from datetime import datetime
import time

from core.analysisRun import analysisRun
from execution.decide_trade import decide_trade
from execution.trend_fatigue_detector import TrendFatigueDetector

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

def main():




    coins = ["ETHUSDT"]

    for coin in coins:

        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        data = analysisRun(coin)

        # 🔥 ejecutar decisión final
        final_trade = decide_trade(data)

        detector = TrendFatigueDetector()

        result = detector.analyze("ETHUSDT", data)


        print(f"\n🪙 {coin} | {time_now}")
        print("DATA:", data)
        print("FINAL TRADE:", final_trade)
        print(result)

        # ⏱️ pausa de 5 segundos
        time.sleep(5)




if __name__ == "__main__":
    main()

