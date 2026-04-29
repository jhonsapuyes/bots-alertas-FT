import json
import os

def saveData(new_data):
    path = "src/baseDatos/datacoins.json"

    os.makedirs(os.path.dirname(path), exist_ok=True)

    # 1. cargar historial existente
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as file:
                history = json.load(file)
        except:
            history = {}
    else:
        history = {}

    # 2. recorrer nuevos datos y agregarlos al historial
    for coin, time_dict in new_data.items():

        if coin not in history:
            history[coin] = {}

        for timestamp, data in time_dict.items():
            history[coin][timestamp] = data

    # 3. guardar todo combinado
    with open(path, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4, ensure_ascii=False)
