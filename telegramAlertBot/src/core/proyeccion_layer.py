


from proyeccion.proyeccion_bajista import proyeccion_bajista
from proyeccion.proyeccion_alcista import proyeccion_alcista


def proyeccionLayer_execute(pt1,pt2,pt3,pt4): 
    resp_proyeccionLayer={}
    resp_proyeccionLayer["proyeccion_alcista"]= proyeccionAlcistaLayer_execute(pt1,pt2,pt3,pt4)
    resp_proyeccionLayer["proyeccion_bajista"]= proyeccionBajistaLayer_execute(pt1,pt2,pt3,pt4)
    return resp_proyeccionLayer


def proyeccionAlcistaLayer_execute(candles,feature,market,trade_plan):
    return proyeccion_alcista(candles,feature,market,trade_plan)

def proyeccionBajistaLayer_execute(candles,feature,market,trade_plan):
    return proyeccion_bajista(candles,feature,market,trade_plan)