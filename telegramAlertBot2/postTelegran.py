import requests

TOKEN = "TU_TOKEN"
CHAT_ID = "TU_CHAT_ID"

def send_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=payload)