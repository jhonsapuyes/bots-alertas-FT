

def calculate_rsi(prices, period=14):
    if len(prices) < period + 1:
        return None

    gains, losses = [], []

    for i in range(1, len(prices)):
        diff = prices[i] - prices[i - 1]
        gains.append(max(diff, 0))
        losses.append(abs(min(diff, 0)))

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period

    if avg_loss <= 1e-12:
        return 100

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def analyze_rsi(rsi):
    if rsi is None:
        return None

    if rsi >= 70:
        return {"indicator": "RSI", "signal": "bearish", "strength": min((rsi - 70) / 30, 1)}

    if rsi <= 30:
        return {"indicator": "RSI", "signal": "bullish", "strength": min((30 - rsi) / 30, 1)}

    return None

