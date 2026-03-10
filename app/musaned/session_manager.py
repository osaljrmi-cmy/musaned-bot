import os
from pathlib import Path
from app.musaned.constants import SESSION_OK, SESSION_MISSING


BASE_DIR = Path(__file__).resolve().parent
STORAGE_STATE_PATH = BASE_DIR / "storage_state.json"


def session_exists() -> bool:
    return STORAGE_STATE_PATH.exists()


def get_session_status() -> str:
    if session_exists():
        return SESSION_OK
    return SESSION_MISSING


def get_storage_state_path() -> str:
    return str(STORAGE_STATE_PATH)


def clear_session_file() -> None:
    if STORAGE_STATE_PATH.exists():
        STORAGE_STATE_PATH.unlink()