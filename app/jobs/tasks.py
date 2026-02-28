from app.flows.state_machine import handle_event

def process_event(wa_id: str, text: str | None, image_media_id: str | None) -> None:
    handle_event(wa_id=wa_id, text=text, image_media_id=image_media_id)
