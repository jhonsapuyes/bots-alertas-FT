

from market_pipeline.feature_engine.engine import engine


def featureLayer_execute(candles):
    resp_featureLayer={}
    resp_featureLayer["feature"]= engine(candles)
    return resp_featureLayer

