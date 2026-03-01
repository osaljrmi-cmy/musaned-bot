from app.sessions.store import get_session, save_session, reset_session, release_lock
from app.whatsapp.cloud_api import send_text
from app.flows import templates
from app.flows.validators import is_cancel, is_yes, is_no, parse_choice

def handle_event(wa_id: str, text: str | None, image_media_id: str | None) -> None:
    session = get_session(wa_id)

    # Global Cancel
    if text and is_cancel(text):
        release_lock(wa_id)
        reset_session(wa_id)
        send_text(wa_id, templates.cancelled())
        return

    # Busy lock (placeholder for future automation)
    if session.lock:
        send_text(wa_id, templates.busy())
        return

    # Image received
    if image_media_id:
        session.last_image_media_id = image_media_id
        session.state = "MENU"
        save_session(session)
        send_text(wa_id, templates.send_image_first_note())
        return

    # Text flow
    if not text:
        if session.state == "IDLE":
            send_text(wa_id, templates.ask_send_image())
        return

    session.last_text = text

    if session.state == "IDLE":
        send_text(wa_id, templates.ask_send_image())
        save_session(session)
        return

    if session.state == "MENU":
        choice = parse_choice(text)
        if not choice:
            send_text(wa_id, templates.invalid_choice())
            return
        session.selected_operation = choice
        session.state = "NEXT_ACTION"
        save_session(session)
        send_text(wa_id, f"✅ تم اختيار العملية رقم {choice}.\\n\\n{templates.next_action_prompt()}")
        return

    if session.state == "NEXT_ACTION":
        if is_yes(text):
            session.state = "MENU"
            save_session(session)
            send_text(wa_id, templates.menu_text())
            return
        if is_no(text):
            reset_session(wa_id)
            send_text(wa_id, templates.ended())
            return
        send_text(wa_id, templates.next_action_prompt())
        return

    # fallback
    session.state = "IDLE"
    save_session(session)
    send_text(wa_id, templates.ask_send_image())
