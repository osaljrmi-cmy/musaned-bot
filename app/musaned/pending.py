from pathlib import Path
import json
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent
PENDING_PATH = BASE_DIR / "pending_supervisor_action.json"


def save_pending_action(
    employee_wa_id: str,
    action_type: str,
    selected_operation: int | None,
    note: str | None = None,
) -> None:
    payload = {
        "employee_wa_id": employee_wa_id,
        "action_type": action_type,
        "selected_operation": selected_operation,
        "note": note,
    }
    PENDING_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def load_pending_action() -> Optional[dict]:
    if not PENDING_PATH.exists():
        return None
    try:
        return json.loads(PENDING_PATH.read_text(encoding="utf-8"))
    except Exception:
        return None


def clear_pending_action() -> None:
    if PENDING_PATH.exists():
        PENDING_PATH.unlink()