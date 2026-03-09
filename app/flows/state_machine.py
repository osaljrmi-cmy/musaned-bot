from app.sessions.store import get_session, save_session, reset_session, release_lock
from app.whatsapp.cloud_api import safe_send_text
from app.flows import templates
from app.flows.validators import is_cancel, is_yes, is_no, parse_choice


def handle_event(wa_id: str, text: str | None, image_media_id: str | None) -> None:
    session = get_session(wa_id)

    # Global cancel
    if text and is_cancel(text):
        release_lock(wa_id)
        reset_session(wa_id)
        safe_send_text(wa_id, templates.cancelled())
        return

    # Busy lock
    if session.lock:
        safe_send_text(wa_id, templates.busy())
        return

    # Image received
    if image_media_id:
        session.last_image_media_id = image_media_id
        session.state = "MENU"
        session.selected_operation = None
        save_session(session)
        safe_send_text(wa_id, templates.send_image_first_note())
        return

    # No text and no image
    if not text:
        if session.state == "IDLE":
            safe_send_text(wa_id, templates.ask_send_image())
        elif session.state == "WAITING_NEW_IMAGE":
            safe_send_text(wa_id, templates.replace_image_prompt())
        return

    session.last_text = text

    # Default state: ask for image
    if session.state == "IDLE":
        safe_send_text(wa_id, templates.ask_send_image())
        save_session(session)
        return

    # User must send replacement image
    if session.state == "WAITING_NEW_IMAGE":
        safe_send_text(wa_id, templates.replace_image_prompt())
        save_session(session)
        return

    # Menu state
    if session.state == "MENU":
        choice = parse_choice(text)
        if not choice:
            safe_send_text(wa_id, templates.invalid_choice())
            return

        session.selected_operation = choice

        # 1) Extract passport data
        if choice == 1:
            if not session.last_image_media_id:
                safe_send_text(wa_id, templates.no_image_yet())
                session.state = "IDLE"
                save_session(session)
                return

            session.state = "NEXT_ACTION"
            save_session(session)

            safe_send_text(
                wa_id,
                f"{templates.session_summary_after_choice(choice)}\n\n"
                f"{templates.extracting_passport()}\n\n"
                f"{templates.passport_extraction_not_ready()}\n\n"
                f"{templates.next_action_prompt()}"
            )
            return

        # 2) Replace image
        if choice == 2:
            session.state = "WAITING_NEW_IMAGE"
            save_session(session)

            safe_send_text(
                wa_id,
                f"{templates.session_summary_after_choice(choice)}\n\n"
                f"{templates.replace_image_prompt()}"
            )
            return

        # 3) End session
        if choice == 3:
            reset_session(wa_id)
            safe_send_text(wa_id, templates.ended())
            return

    # Ask if another action is needed
    if session.state == "NEXT_ACTION":
        if is_yes(text):
            session.state = "MENU"
            save_session(session)
            safe_send_text(wa_id, templates.menu_text())
            return

        if is_no(text):
            reset_session(wa_id)
            safe_send_text(wa_id, templates.ended())
            return

        safe_send_text(wa_id, templates.next_action_prompt())
        return

    # Fallback
    session.state = "IDLE"
    save_session(session)
    safe_send_text(wa_id, templates.ask_send_image())