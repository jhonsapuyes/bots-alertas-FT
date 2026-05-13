


from adaptive_context.adaptive_context import adaptive_context


def adaptiveContextLayer_execute(pt1,pt2,pt3):
    resp_adaptiveContextLayer={}
    resp_adaptiveContextLayer["adaptive_context"]= adaptiveContext(pt1["features"],pt2,pt3)
    return resp_adaptiveContextLayer

def adaptiveContext(features,regime,signal):
    return adaptive_context(features, regime, signal)
