

import json
import os

STATE_FILE = "src/baseDatos/trade_state.json"


def save_state(risk):
    data = {
        "capital": risk.capital,
        "peak_capital": risk.peak_capital,
        "in_position": risk.in_position,
        "position": risk.position,
        "trading_enabled": getattr(risk, "trading_enabled", True)
    }

    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=4)


def load_state(risk):
    if not os.path.exists(STATE_FILE):
        return

    with open(STATE_FILE, "r") as f:
        data = json.load(f)

    risk.capital = data.get("capital", risk.capital)
    risk.peak_capital = data.get("peak_capital", risk.peak_capital)
    risk.in_position = data.get("in_position", False)
    risk.position = data.get("position", None)
    risk.trading_enabled = data.get("trading_enabled", True)

