from typing import Any, Dict, Optional, Tuple

def parse_webhook(payload: Dict[str, Any]) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """"Return (wa_id, text, image_media_id) from Meta webhook payload."""
    try:
        entry = payload.get(""entry"", [])[0]
        changes = entry.get(""changes"", [])[0]
        value = changes.get(""value"", {})
        messages = value.get(""messages"", [])
        if not messages:
            return None, None, None

        msg = messages[0]
        wa_id = msg.get(""from"")
        msg_type = msg.get(""type"")

        if msg_type == ""text"":
            text = msg.get(""text"", {}).get(""body"")
            return wa_id, text, None

        if msg_type == ""image"":
            image_media_id = msg.get(""image"", {}).get(""id"")
            return wa_id, None, image_media_id

        return wa_id, None, None

    except Exception:
        return None, None, None
