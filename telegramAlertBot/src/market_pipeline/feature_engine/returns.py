

def calculate_returns(candles):
    returns = []

    for i in range(1, len(candles)):
        prev_close = candles[i - 1]["close"]
        curr_close = candles[i]["close"]

        r = (curr_close - prev_close) / prev_close
        returns.append(r)

    return returns

