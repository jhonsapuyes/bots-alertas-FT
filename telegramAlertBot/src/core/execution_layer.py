



from execution.execution import execute_trade_plan
from protetion_execution.protetion_execution import protect_execution


def executionLayer_execute(pt1):
    resp_executionLayer={}
    resp_executionLayer["execute_traderPlan"]= execute_traderPlan(pt1)
    resp_executionLayer["execute_protect"]= execute_protect(resp_executionLayer["execute_traderPlan"])
    return resp_executionLayer

def execute_traderPlan(trade_plan):
    return execute_trade_plan(
    trade_plan=trade_plan,
    exchange="binance",
    symbol="ETHUSDT"
    )


def execute_protect(execution_result):
    return protect_execution(execution_result)

