

import uuid
from baseDatos.trade_logger import log_trade
from datetime import datetime

class RiskManager:

    def __init__(self, capital, risk_per_trade=0.01, max_drawdown=0.2):
        self.initial_capital = capital
        self.capital = capital
        self.risk_per_trade = risk_per_trade
        self.max_drawdown = max_drawdown

        self.peak_capital = capital
        self.in_position = False
        self.position = None

        self.trading_enabled = True

    # 🧮 tamaño de posición
    def calculate_position_size(self, entry, stop_loss):
        risk_amount = self.capital * self.risk_per_trade
        risk_per_unit = abs(entry - stop_loss)

        if risk_per_unit == 0:
            return 0

        size = risk_amount / risk_per_unit
        return round(size, 6)

    # 🟢 abrir operación
    def open_trade(self, price, signal, coin):

        if self.in_position or not self.trading_enabled:
            return None

        if signal["buy"]:
            stop_loss = price * 0.98
            take_profit = price * 1.04

        elif signal["sell"]:
            stop_loss = price * 1.02
            take_profit = price * 0.96

        else:
            return None

        size = self.calculate_position_size(price, stop_loss)

        if size <= 0:
            return None

        trade_id = str(uuid.uuid4())

        self.position = {
            "opened_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "id": trade_id,
            "coin": coin,  # 🔥 CLAVE
            "entry": price,
            "size": size,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "type": "long" if signal["buy"] else "short"
        }

        self.in_position = True

        print(f"🟢 OPEN {coin} {self.position['type']} | id={trade_id} entry={price} size={size}")
        return self.position

    # 🔴 cerrar operación
    def close_trade(self, price, reason, coin):

        if not self.in_position:
            return

        # 🚨 protección multi-coin
        if self.position["coin"] != coin:
            return

        entry = self.position["entry"]
        size = self.position["size"]
        trade_type = self.position["type"]

        if trade_type == "long":
            pnl = (price - entry) * size
        else:
            pnl = (entry - price) * size

        # comisión simple
        fee = price * size * 0.001
        pnl -= fee

        self.capital += pnl

        print(f"🔴 CLOSE {coin} {trade_type} | price={price} PnL={round(pnl,2)} reason={reason}")
        print(f"💰 Capital: {round(self.capital,2)}")

        log_trade(self.position, price, pnl, reason)

        self.in_position = False
        self.position = None

        self.update_drawdown()

    # 📉 drawdown
    def update_drawdown(self):
        if self.capital > self.peak_capital:
            self.peak_capital = self.capital

        drawdown = (self.peak_capital - self.capital) / self.peak_capital

        if drawdown >= self.max_drawdown:
            print("⛔ MAX DRAWDOWN alcanzado. STOP TRADING")
            self.trading_enabled = False

    # 🔄 gestionar trade
    def manage_trade(self, price, coin):

        if not self.in_position:
            return

        # 🚨 protección multi-coin
        if self.position["coin"] != coin:
            return

        sl = self.position["stop_loss"]
        tp = self.position["take_profit"]
        trade_type = self.position["type"]

        if trade_type == "long":
            if price <= sl:
                self.close_trade(price, "stop_loss", coin)
            elif price >= tp:
                self.close_trade(price, "take_profit", coin)

        else:
            if price >= sl:
                self.close_trade(price, "stop_loss", coin)
            elif price <= tp:
                self.close_trade(price, "take_profit", coin)

