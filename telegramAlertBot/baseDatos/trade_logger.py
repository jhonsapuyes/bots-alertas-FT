

import json
import os

LOG_FILE = "src/baseDatos/trade_log.json"


def log_trade(trade, exit_price, pnl, reason):
    log = []

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            log = json.load(f)

    record = {
        "id": trade["id"],
        "type": trade["type"],
        "entry": trade["entry"],
        "exit": exit_price,
        "size": trade["size"],
        "pnl": pnl,
        "reason": reason
    }

    log.append(record)

    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=4)

