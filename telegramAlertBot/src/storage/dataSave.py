

import os
import json
from datetime import datetime

def save_pipeline_snapshot(symbol: str, data: dict):

    folder_path = "./dataSave"
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, "datos.json")

    # -------------------------
    # 1. KEY DE TIEMPO
    # -------------------------
    now = datetime.now()
    time_key = now.strftime("%Y-%m-%d/%H:%M:%S")

    # -------------------------
    # 2. CARGAR DATA EXISTENTE
    # -------------------------
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                store = json.load(f)
        except json.JSONDecodeError:
            store = {}
    else:
        store = {}

    # -------------------------
    # 3. ASEGURAR ESTRUCTURA POR SYMBOL
    # -------------------------
    if symbol not in store:
        store[symbol] = {}

    # -------------------------
    # 4. GUARDAR SNAPSHOT
    # -------------------------
    store[symbol][time_key] = data

    # -------------------------
    # 5. ESCRIBIR ARCHIVO
    # -------------------------
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(store, f, indent=4, ensure_ascii=False)

    print(f"Snapshot guardado: {symbol} -> {time_key}")
    return file_path

