

import numpy as np

class TrendFatigueDetector:

    def __init__(self):
        self.history = {}

    def update(self, symbol, data):

        if symbol not in self.history:
            self.history[symbol] = []

        self.history[symbol].append({
            "adx": data["adx"],
            "macd": data["macd"] - data["signal"],  # histograma
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

        # 🔥 FIX CLAVE: evitar falso "building"
        if len(hist) < 5:
            if data.get("adx", 0) > 25:
                return {"phase": "trend", "strength": "developing"}
            return {"phase": "building", "strength": "low"}

        # =========================
        # 📊 SLOPES
        # =========================
        adx_values = [h["adx"] for h in hist]
        macd_values = [h["macd"] for h in hist]
        rsi_values = [h["rsi"] for h in hist]
        price_sma_values = [h["price_sma"] for h in hist]

        adx_slope = self._slope(adx_values)
        macd_slope = self._slope(macd_values)
        rsi_slope = self._slope(rsi_values)
        price_sma_slope = self._slope(price_sma_values)

        score = 0

        # 🚀 ACELERACIÓN
        if adx_slope > 0 and macd_slope > 0:
            score += 2

        if adx_slope > 0.5:
            score += 1

        # 🟡 DEBILITAMIENTO
        if adx_slope < 0:
            score -= 1

        if rsi_slope < 0:
            score -= 1

        # 🔴 DIVERGENCIA
        if macd_slope < 0 and price_sma_slope > 0:
            score -= 2

        # 🔴 PÉRDIDA DE FUERZA
        if adx_slope < 0 and abs(macd_slope) < 0.2:
            score -= 2

        # 🔴 REBOTE DÉBIL
        if rsi_values[-1] < 40 and rsi_slope < 0:
            score -= 1

        # =========================
        # 🎯 CLASIFICACIÓN
        # =========================
        if score >= 3:
            return {"phase": "accelerating", "strength": "strong", "score": score}

        elif score == 2:
            return {"phase": "trend", "strength": "medium", "score": score}

        elif score == 1:
            return {"phase": "mature", "strength": "weak", "score": score}

        else:
            return {"phase": "exhaustion", "strength": "exit", "score": score}          

