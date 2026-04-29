

import requests
import time


def get_market_data(symbol="BTCUSDT", interval="1h", limit=500, retries=3):

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

            if not isinstance(data, list) or len(data) < 50:
                return []

            candles = []

            for c in data:
                try:
                    close = float(c[4])
                    high = float(c[2])
                    low = float(c[3])
                    volume = float(c[5])

                    if high <= 0 or low <= 0 or close <= 0:
                        continue

                    candles.append({
                        "close": close,
                        "high": high,
                        "low": low,
                        "volume": volume
                    })

                except Exception as e:
                    print("Candle parse error:", e)
                    continue

            return candles

        except Exception as e:
            print("Request error:", e)
            time.sleep(1)

    return []

