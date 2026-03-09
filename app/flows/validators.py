def is_cancel(text: str) -> bool:
    t = text.strip().lower()
    return t in ["إلغاء", "الغاء", "cancel"]


def is_yes(text: str) -> bool:
    t = text.strip().lower()
    return t in ["نعم", "1", "yes", "y"]


def is_no(text: str) -> bool:
    t = text.strip().lower()
    return t in ["لا", "2", "no", "n"]


def parse_choice(text: str):
    t = text.strip()
    if t.isdigit():
        n = int(t)
        if 1 <= n <= 3:
            return n
    return None