import requests
from config.config_loader import CONFIG

def send_telegram(msg):

    if not CONFIG.alerts.telegram.enabled:
        return

    url = f"https://api.telegram.org/bot{CONFIG.alerts.telegram.bot_token}/sendMessage"

    requests.post(url, data={
        "chat_id": CONFIG.alerts.telegram.chat_id,
        "text": msg
    })
