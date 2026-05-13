

from market_pipeline.data_fetch.get_market_data import get_market_data
from market_pipeline.data_fetch.data_adapter import normalize_candles


def DataLayer_execute(pt1,pt2,pt3):
    resp_dataLayer={}
    resp_dataLayer["raw_data"]= getData(pt1,pt2,pt3)
    resp_dataLayer["candles"]= buildCandles(resp_dataLayer["raw_data"])
    return resp_dataLayer


def getData(symbol,interval,limit):
    return get_market_data(symbol=symbol,interval=interval,limit=10,retries=3)

def buildCandles(raw_data):
    return normalize_candles(raw_data)

