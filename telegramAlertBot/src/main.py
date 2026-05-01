

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
from market_pipeline.feature_engine.engine import engine

def main1(): # esta solo esta haciendo analisis a la data

    raw_data = get_market_data("ETHUSDT")
    print("get_market_data:", raw_data)

    features = engine(raw_data)
    print("engine:", features)


from core.pipeline import run_pipeline
from market_pipeline.feature_engine.data_adapter import normalize_candles
from market_pipeline.feature_engine.engine import engine


def main():

    raw_data = get_market_data()

    candles = normalize_candles(raw_data)

    # 🔥 ENGINE CORRECTO
    engine_output = engine(candles)


    # 🔥 PIPELINE recibe dict, no list
    result = run_pipeline(engine_output)

    print("\n🔥 RESULTADO FINAL:")
    print(result)

if __name__ == "__main__":
    main()