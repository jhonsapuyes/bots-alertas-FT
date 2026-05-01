

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

def main():

    raw_data = get_market_data("ETHUSDT")
    print("get_market_data:", raw_data)

    features = engine(raw_data)
    print("engine:", features)


if __name__ == "__main__":
    main()

