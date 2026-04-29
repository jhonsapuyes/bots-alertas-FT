

import numpy as np

import numpy as np

class TrendFatigueDetector:

    def __init__(self):
        self.history = {}

    def update(self, symbol, data):

        if symbol not in self.history:
            self.history[symbol] = []

        self.history[symbol].append({
            "adx": data["adx"],
            "macd": data["macd"] - data["signal"],
            "rsi": data["rsi"],
            "price_sma": data["price"] - data["sma"]
        })

        if len(self.history[symbol]) > 10:
            self.history[symbol].pop(0)

    def _slope(self, values):
        if len(values) < 3:
            return 0
        x = np.arange(len(values))
        return np.polyfit(x, values, 1)[0]

    def analyze(self, symbol, data):

        self.update(symbol, data)
        hist = self.history[symbol]

        if len(hist) < 5:
            return {"phase": "building", "strength": "low"}

        adx_slope = self._slope([h["adx"] for h in hist])
        macd_slope = self._slope([h["macd"] for h in hist])
        rsi_slope = self._slope([h["rsi"] for h in hist])

        score = 0

        if adx_slope > 0 and macd_slope > 0:
            score += 2

        if adx_slope > 0.5:
            score += 1

        if adx_slope < 0:
            score -= 1

        if rsi_slope < 0:
            score -= 1

        if score >= 3:
            return {"phase": "accelerating", "strength": "strong"}

        elif score == 2:
            return {"phase": "trend", "strength": "medium"}

        elif score == 1:
            return {"phase": "mature", "strength": "weak"}

        else:
            return {"phase": "exhaustion", "strength": "exit"}
        
