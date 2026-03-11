from pathlib import Path
import json
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent
STATE_FILE = BASE_DIR / "admin_pending_session.json"


def save_admin_pending_session(
    employee_wa_id: str,
    selected_operation: int | None,
    status: str,
    note: str | None = None,
) -> None:
    payload = {
        "employee_wa_id": employee_wa_id,
        "selected_operation": selected_operation,
        "status": status,
        "note": note,
        "supervisor_done": False,
        "otp_code": None,
    }

    STATE_FILE.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_admin_pending_session() -> Optional[dict]:
    if not STATE_FILE.exists():
        return None

    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return None


def clear_admin_pending_session() -> None:
    if STATE_FILE.exists():
        STATE_FILE.unlink()


def mark_supervisor_done() -> bool:
    state = load_admin_pending_session()
    if not state:
        return False

    state["supervisor_done"] = True

    STATE_FILE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return True


def set_otp_code(code: str) -> bool:
    state = load_admin_pending_session()
    if not state:
        return False

    state["otp_code"] = code

    STATE_FILE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return True