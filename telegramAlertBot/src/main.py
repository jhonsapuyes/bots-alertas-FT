

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




from core.adaptiveContext_layer import adaptiveContextLayer_execute
from core.data_layer import DataLayer_execute
from core.execution_layer import executionLayer_execute
from core.feature_layer import featureLayer_execute
from core.marketAnalysis_layer import marketAnalysisLayer_execute
from core.proyeccion_layer import proyeccionLayer_execute
from core.strategyContext_layer import strategyContextLayer_execute
from core.strategy_layer import strategyLayer_execute
from storage.dataSave import save_pipeline_snapshot


def main():
    input_dataSave = {}

    symbol= "ETHUSDT"
    interval= "1h"
    limit= 30

    resp_datalayer= DataLayer_execute(symbol,interval,limit)
    input_dataSave["datalayer"] = resp_datalayer

    resp_featureLayer= featureLayer_execute(resp_datalayer["candles"])
    input_dataSave["featureLayer"] = resp_featureLayer

    resp_marketAnalysisLayer= marketAnalysisLayer_execute(resp_featureLayer["feature"])
    input_dataSave["marketAnalysisLayer"] = resp_marketAnalysisLayer

    resp_strategyLayer= strategyLayer_execute(resp_featureLayer["feature"],resp_marketAnalysisLayer)
    input_dataSave["strategy"] = resp_strategyLayer["strategy"]


    def executionPlanner(trade_plan):
        resp_executionLayer= executionLayer_execute(trade_plan)
        #print("main-resp_executionLayer", resp_executionLayer["execute_traderPlan"])
        #print("main-resp_executionLayer", resp_executionLayer["execute_protect"])

    if(resp_strategyLayer["strategy"]["valid"] == False):
        resp_adaptiveContextLayer= adaptiveContextLayer_execute(resp_featureLayer["feature"],resp_marketAnalysisLayer["regime"],resp_marketAnalysisLayer["signal"])
        input_dataSave["adaptiveContext"] = resp_strategyLayer

        resp_strategyContextLayer = strategyContextLayer_execute(
            resp_featureLayer["feature"],
            resp_marketAnalysisLayer,
            resp_adaptiveContextLayer["adaptive_context"]
        )
        input_dataSave["strategyContext"] = resp_strategyContextLayer["strategy_context"]
        input_dataSave["tradePlan_context"] = resp_strategyContextLayer["tradePlan_context"]
        #print(resp_strategyContextLayer["tradePlan_context"])

        resp_proyeccionLayer= proyeccionLayer_execute(
            input_dataSave["datalayer"]["candles"],
            input_dataSave["featureLayer"]["feature"],
            input_dataSave["marketAnalysisLayer"],
            resp_strategyContextLayer["tradePlan_context"]
        )
        input_dataSave["proyeccion"] = resp_proyeccionLayer
        #executionPlanner(resp_strategyContextLayer["tradePlan_context"])

    elif(resp_strategyLayer["strategy"]["valid"] == True):
        input_dataSave["trade_plan"] = resp_strategyLayer["trade_plan"]
        resp_proyeccionLayer= proyeccionLayer_execute(
            input_dataSave["datalayer"]["candles"],
            input_dataSave["featureLayer"]["feature"],
            input_dataSave["marketAnalysisLayer"],
            input_dataSave["trade_plan"]
        )
        input_dataSave["proyeccion"] = resp_proyeccionLayer
        #executionPlanner(resp_strategyLayer["trade_plan"])

    save_pipeline_snapshot(symbol,input_dataSave)



    #print("main-resp_proyeccionLayer",resp_proyeccionLayer)

    #print(input_dataSave)


if __name__ == "__main__":
    main()
