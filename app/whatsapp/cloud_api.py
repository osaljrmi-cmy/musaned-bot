import requests # type: ignore
from app.settings import settings

GRAPH = "https://graph.facebook.com/v21.0"


def send_text(to_wa_id: str, text: str) -> None:
    url = f"{GRAPH}/{settings.PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to_wa_id,
        "type": "text",
        "text": {"body": text},
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()