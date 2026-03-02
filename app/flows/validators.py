def _norm(text: str) -> str:
    return (text or "").strip().lower()


def is_cancel(text: str) -> bool:
    t = _norm(text)
    return t in ["إلغاء", "الغاء", "cancel"]


def is_yes(text: str) -> bool:
    t = _norm(text)
    return t in ["نعم", "yes", "y", "1"]


def is_no(text: str) -> bool:
    t = _norm(text)
    return t in ["لا", "no", "n", "2"]


def parse_choice(text: str) -> int | None:
    """
    Menu choice: 1..5
    """
    t = _norm(text)
    if t.isdigit():
        n = int(t)
        if 1 <= n <= 5:
            return n
    return None