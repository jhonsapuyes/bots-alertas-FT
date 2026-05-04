

import requests
import time

def get_market_data(symbol="ETHUSDT", interval="1h", limit=10, retries=3):

    url = "https://api.binance.com/api/v3/klines"

    for _ in range(retries):
        try:
            response = requests.get(url, params={
                "symbol": symbol,
                "interval": interval,
                "limit": limit
            }, timeout=10)

            if response.status_code == 429:
                time.sleep(2)
                continue

            if response.status_code != 200:
                print("API error:", response.status_code)
                return []

            data = response.json()

            if not isinstance(data, list) or len(data) < 10:
                return []

            candles = []

            for c in data:
                try:
                    candles.append({
                        # =========================
                        # 📊 OHLCV COMPLETO
                        # =========================
                        "timestamp": c[0],          # Open time
                        "open": float(c[1]),
                        "high": float(c[2]),
                        "low": float(c[3]),
                        "close": float(c[4]),
                        "volume": float(c[5]),

                        # =========================
                        # 🧠 EXTRA ÚTIL (OPCIONAL PERO CLAVE)
                        # =========================
                        "close_time": c[6],
                        "quote_volume": float(c[7]),
                        "trades": int(c[8]),
                        "taker_buy_base": float(c[9]),
                        "taker_buy_quote": float(c[10])
                    })

                except Exception as e:
                    print("Candle parse error:", e)
                    continue

            return candles

        except Exception as e:
            print("Request error:", e)
            time.sleep(1)

