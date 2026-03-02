import os
import requests


GRAPH = "https://graph.facebook.com/v21.0"


def send_text(to_wa_id: str, text: str) -> None:
    """
    Sends a real WhatsApp message using Cloud API.
    Raises exception if sending fails.
    """
    whatsapp_token = os.getenv("WHATSAPP_TOKEN")
    phone_number_id = os.getenv("PHONE_NUMBER_ID")

    if not whatsapp_token or not phone_number_id:
        raise RuntimeError("WhatsApp credentials are not configured")

    url = f"{GRAPH}/{phone_number_id}/messages"

    headers = {
        "Authorization": f"Bearer {whatsapp_token}",
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


def safe_send_text(to_wa_id: str, text: str) -> None:
    """
    Safe wrapper that never crashes the worker.
    If WhatsApp is not configured, prints message instead.
    """
    try:
        send_text(to_wa_id, text)
    except Exception as e:
        print(f"[mock-send] to={to_wa_id} text={text}")
        print(f"[mock-send] reason={e}", flush=True)