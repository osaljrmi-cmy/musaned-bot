from app.sessions.store import get_session, save_session, reset_session, release_lock
from app.whatsapp.cloud_api import safe_send_text
from app.flows import templates
from app.flows.validators import (
    is_cancel,
    is_yes,
    is_no,
    parse_choice,
    is_done,
    parse_otp_command,
)
from app.settings import settings
from app.musaned.service import ensure_musaned_session
from app.musaned.constants import (
    SESSION_OK,
    CAPTCHA_REQUIRED,
    OTP_REQUIRED,
    LOGIN_SUCCESS,
)
from app.musaned.pending import save_pending_action, load_pending_action, clear_pending_action


def _handle_supervisor_message(wa_id: str, text: str | None) -> bool:
    if not settings.SUPERVISOR_WA_ID:
        return False

    if wa_id != settings.SUPERVISOR_WA_ID:
        return False

    pending = load_pending_action()
    if not pending:
        safe_send_text(wa_id, templates.no_pending_supervisor_action())
        return True

    if text and is_done(text):
        clear_pending_action()
        safe_send_text(wa_id, templates.supervisor_done_ack())
        safe_send_text(
            pending["employee_wa_id"],
            "تم استلام تأكيد المشرف بحل الكابتشا. سنربط استكمال التنفيذ في الخطوة التالية."
        )
        return True

    otp_code = parse_otp_command(text or "")
    if otp_code:
        clear_pending_action()
        safe_send_text(wa_id, templates.supervisor_otp_ack(otp_code))
        safe_send_text(
            pending["employee_wa_id"],
            f"تم استلام رمز التحقق {otp_code}. سنربط استكمال التنفيذ في الخطوة التالية."
        )
        return True

    safe_send_text(
        wa_id,
        "أمر غير معروف للمشرف.\nأرسل:\n- تم\nأو\n- رمز 123456"
    )
    return True


def _start_musaned_session_flow(wa_id: str, session) -> bool:
    safe_send_text(wa_id, templates.musaned_session_expired())

    result = ensure_musaned_session(headless=False)

    if result in (SESSION_OK, LOGIN_SUCCESS):
        safe_send_text(wa_id, templates.musaned_session_ready())
        return True

    if result == CAPTCHA_REQUIRED:
        session.state = "WAITING_MUSANED_CAPTCHA"
        session.pending_musaned_status = CAPTCHA_REQUIRED
        save_session(session)

        save_pending_action(
            employee_wa_id=wa_id,
            action_type=CAPTCHA_REQUIRED,
            selected_operation=session.selected_operation,
            note="Supervisor must solve captcha",
        )

        safe_send_text(wa_id, templates.musaned_captcha_required())

        if settings.SUPERVISOR_WA_ID:
            safe_send_text(
                settings.SUPERVISOR_WA_ID,
                templates.supervisor_captcha_message(wa_id, session.selected_operation),
            )
        return False

    if result == OTP_REQUIRED:
        session.state = "WAITING_MUSANED_OTP"
        session.pending_musaned_status = OTP_REQUIRED
        save_session(session)

        save_pending_action(
            employee_wa_id=wa_id,
            action_type=OTP_REQUIRED,
            selected_operation=session.selected_operation,
            note="Supervisor must send OTP",
        )

        safe_send_text(wa_id, templates.musaned_otp_required())

        if settings.SUPERVISOR_WA_ID:
            safe_send_text(
                settings.SUPERVISOR_WA_ID,
                templates.supervisor_otp_message(wa_id, session.selected_operation),
            )
        return False

    safe_send_text(wa_id, templates.musaned_login_failed())
    return False


def handle_event(wa_id: str, text: str | None, image_media_id: str | None) -> None:
    if _handle_supervisor_message(wa_id, text):
        return

    session = get_session(wa_id)

    if text and is_cancel(text):
        release_lock(wa_id)
        reset_session(wa_id)
        safe_send_text(wa_id, templates.cancelled())
        return

    if session.lock:
        safe_send_text(wa_id, templates.busy())
        return

    if image_media_id:
        session.last_image_media_id = image_media_id
        session.state = "MENU"
        session.selected_operation = None
        save_session(session)
        safe_send_text(wa_id, templates.send_image_first_note())
        return

    if not text:
        if session.state == "IDLE":
            safe_send_text(wa_id, templates.ask_send_image())
        elif session.state == "WAITING_NEW_IMAGE":
            safe_send_text(wa_id, templates.replace_image_prompt())
        return

    session.last_text = text

    if session.state == "IDLE":
        safe_send_text(wa_id, templates.ask_send_image())
        save_session(session)
        return

    if session.state == "WAITING_NEW_IMAGE":
        safe_send_text(wa_id, templates.replace_image_prompt())
        save_session(session)
        return

    if session.state == "WAITING_MUSANED_CAPTCHA":
        safe_send_text(wa_id, "ما زلنا بانتظار تدخل المشرف لحل الكابتشا.")
        return

    if session.state == "WAITING_MUSANED_OTP":
        safe_send_text(wa_id, "ما زلنا بانتظار إدخال رمز التحقق من المشرف.")
        return

    if session.state == "MENU":
        choice = parse_choice(text)
        if not choice:
            safe_send_text(wa_id, templates.invalid_choice())
            return

        session.selected_operation = choice
        save_session(session)

        if choice == 6:
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

        if choice == 2:
            session.state = "NEXT_ACTION"
            save_session(session)

            ok = _start_musaned_session_flow(wa_id, session)
            if ok:
                safe_send_text(
                    wa_id,
                    f"{templates.session_summary_after_choice(choice)}\n\n"
                    "تم التحقق من جاهزية جلسة مساند. سنربط تنفيذ حذف المرشح في الخطوة التالية.\n\n"
                    f"{templates.next_action_prompt()}"
                )
            return

        if choice in (1, 3, 4, 5):
            session.state = "NEXT_ACTION"
            save_session(session)

            ok = _start_musaned_session_flow(wa_id, session)
            if ok:
                safe_send_text(
                    wa_id,
                    f"{templates.session_summary_after_choice(choice)}\n\n"
                    "تم التحقق من جاهزية جلسة مساند. سنربط تنفيذ العملية في الخطوة التالية.\n\n"
                    f"{templates.next_action_prompt()}"
                )
            return

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

    session.state = "IDLE"
    save_session(session)
    safe_send_text(wa_id, templates.ask_send_image())