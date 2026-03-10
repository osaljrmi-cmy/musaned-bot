from app.musaned.constants import (
    SESSION_OK,
    SESSION_MISSING,
)
from app.musaned.session_manager import get_session_status
from app.musaned.login import login_to_musaned


def ensure_musaned_session(headless: bool = False) -> str:
    session_status = get_session_status()

    if session_status == SESSION_OK:
        return SESSION_OK

    login_result = login_to_musaned(headless=headless)
    return login_result