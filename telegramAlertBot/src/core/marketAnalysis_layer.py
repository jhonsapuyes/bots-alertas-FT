

from confirmation_filter.confirmation_filter import evaluate_confirmation
from opportunity_engine.opportunity_engine import run_opportunity_engine
from signal_translation.signal_translator import translate_signal
from regime_engine.regime_classifier import classify_regime


def marketAnalysisLayer_execute(pt1):    
    resp_marketAnalysisLayer={}
    resp_marketAnalysisLayer["regime"]= regime(pt1)
    resp_marketAnalysisLayer["opportunity"]= opportunity(pt1,resp_marketAnalysisLayer["regime"])
    resp_marketAnalysisLayer["signal"]= signal(resp_marketAnalysisLayer["opportunity"],pt1["features"],resp_marketAnalysisLayer["regime"])
    resp_marketAnalysisLayer["confirmation"]= confirmation(pt1["features"],resp_marketAnalysisLayer["regime"],resp_marketAnalysisLayer["signal"],resp_marketAnalysisLayer["opportunity"])
    return resp_marketAnalysisLayer


def regime(feature):
        return classify_regime(feature)


def opportunity(feature,regime):
    return run_opportunity_engine(feature,regime)


def signal(opportunities,features,regime):
    signals = []
    for opp in opportunities:
        print()
        signal = translate_signal(opp,features,regime)
        signals.append(signal)
    return signals


def confirmation(features,regime,signal,opportunities):
    return evaluate_confirmation({"features": features,"regime": regime,"signal": signal[0],"opportunity": opportunities[0]})

