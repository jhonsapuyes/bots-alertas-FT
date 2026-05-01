

import json
import os
from datetime import datetime

SIGNAL_FILE = "src/baseDatos/signals.json"


def log_signal_from_trade(trade):
    """
    Guarda una señal basada en un trade real (con entry, SL, TP)
    """

    data = []

    # cargar historial si existe
    if os.path.exists(SIGNAL_FILE):
        with open(SIGNAL_FILE, "r") as f:
            data = json.load(f)

    # 🚨 evitar duplicados (muy importante si reinicias el bot)
    if data and data[-1].get("id") == trade["id"]:
        return

    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "id": trade["id"],
        "coin": trade["coin"],
        "entry": trade["entry"],
        "stop_loss": trade["stop_loss"],
        "take_profit": trade["take_profit"],
        "type": trade["type"]
    }

    data.append(record)

    # guardar
    with open(SIGNAL_FILE, "w") as f:
        json.dump(data, f, indent=4)

